import os
import bpy
import addon_utils


def _has_pykeentools() -> bool:
    """Check if pykeentools can be imported."""
    try:
        import pykeentools  # type: ignore
    except Exception as exc:  # pragma: no cover - Blender runtime
        print("pykeentools missing:", exc)
        return False
    print("pykeentools OK:", getattr(pykeentools, "__file__", "unknown"))
    return True


def _op_label(op) -> str:
    """Best-effort human-readable label for an operator."""
    try:
        name = op.idname()
        if name:
            return name
    except Exception:
        pass
    try:
        return op.__name__
    except Exception:
        return str(op)


def _op_exists(op) -> bool:
    """Check that an operator is registered and usable."""
    if op is None:
        return False
    try:
        op.get_rna_type()
        return True
    except Exception as exc:  # pragma: no cover - Blender runtime
        print("Operator not available:", op, exc)
        return False


def _call_op(op, **kwargs) -> bool:
    """Call a Blender operator safely, filtering kwargs to existing props."""
    if not _op_exists(op):
        return False
    try:
        props = op.get_rna_type().properties
    except Exception as exc:  # pragma: no cover - Blender runtime
        print("Failed to read operator props:", op, exc)
        return False

    clean = {k: v for k, v in kwargs.items() if k in props}
    label = _op_label(op)
    print("Calling", label, clean)
    try:
        # Prefer direct execute mode in background to avoid UI dialogs.
        res = op('EXEC_DEFAULT', **clean)
        print("Result EXEC_DEFAULT", res)
        return True
    except Exception as exc:  # pragma: no cover - Blender runtime
        print("EXEC_DEFAULT failed for", label, exc)
        try:
            res = op(**clean)
            print("Result default", res)
            return True
        except Exception as exc2:  # pragma: no cover - Blender runtime
            print("Failed", label, exc2)
            return False


def _ensure_keentools_enabled() -> None:
    """Ensure the KeenTools addon is enabled so its operators are available."""
    try:
        addon_utils.modules(refresh=True)
    except Exception as exc:
        print("addon_utils.modules refresh failed:", exc)

    enabled, loaded = addon_utils.check("keentools")
    print(f"keentools addon status: enabled={enabled}, loaded={loaded}")

    if not enabled:
        print("Enabling KeenTools addon (keentools)")
        try:
            # Via operator
            bpy.ops.preferences.addon_enable(module="keentools")
        except Exception as exc:
            print("bpy.ops.preferences.addon_enable failed:", exc)
            try:
                # Fallback via addon_utils
                addon_utils.enable("keentools", default_set=True, persistent=True)
            except Exception as exc2:
                print("addon_utils.enable failed:", exc2)

    try:
        bpy.ops.wm.save_userpref()
    except Exception as exc:
        print("save_userpref in _ensure_keentools_enabled failed:", exc)

    # Try to reload scripts to make sure operators are registered
    try:
        bpy.ops.script.reload()
    except Exception:
        pass


def _try_install_core() -> bool:
    """Install KeenTools core.

    Returns:
        True if an installation was attempted (and should trigger a restart),
        False if we could not even start installation (no operators, no core path, etc.).
    """
    ops = bpy.ops.keentools_preferences
    names = sorted(n for n in dir(ops) if "install" in n or "download" in n or "pkt" in n)
    print("KeenTools preference ops:", names)

    core_path = os.environ.get("KEENTOOLS_CORE_PATH", "").strip()
    product = int(os.environ.get("KEENTOOLS_PRODUCT", "0"))
    allow_online = os.environ.get("KEENTOOLS_ALLOW_ONLINE", "1").strip() != "0"

    print("KEENTOOLS_CORE_PATH:", core_path or "<empty>")
    print("KEENTOOLS_PRODUCT:", product)
    print("KEENTOOLS_ALLOW_ONLINE:", allow_online)

    # Offline .pkt first if provided, then optional online.
    candidates = []
    if core_path:
        candidates.extend(["install_pkt_from_file", "install_pkt_from_file_with_warning"])
    elif allow_online:
        candidates.append("install_latest_pkt")

    attempted = False

    # **PRIMARY METHOD**: Direct installation via InstallationProgress (offline mode)
    if core_path:
        print("Attempting direct core installation via InstallationProgress")
        try:
            # Import the InstallationProgress class directly from keentools preferences
            import sys
            addon_path = bpy.utils.user_resource('SCRIPTS', path='addons')
            keentools_path = os.path.join(addon_path, 'keentools')
            if keentools_path not in sys.path:
                sys.path.insert(0, keentools_path)
            
            # Try direct import from preferences.progress module
            try:
                from preferences.progress import InstallationProgress
            except ImportError:
                # Fallback: try importing from keentools.preferences.progress
                from keentools.preferences.progress import InstallationProgress
            
            print(f"Starting zip install from: {core_path}")
            InstallationProgress.start_zip_install(core_path)
            print("✓ Direct core installation completed successfully")
            
            try:
                bpy.ops.wm.save_userpref()
            except Exception as exc:
                print("save_userpref after direct core install failed:", exc)
            
            return True
        except Exception as exc:
            print(f"✗ Direct core install failed: {exc}")
            print("  Falling back to operator-based installation...")

    # **FALLBACK METHOD**: Use KeenTools operators (for online mode or if direct fails)
    for name in candidates:
        op = getattr(ops, name, None)
        if not _op_exists(op):
            continue

        kwargs = {}
        try:
            props = op.get_rna_type().properties
        except Exception as exc:  # pragma: no cover - Blender runtime
            print("Failed to read operator props:", name, exc)
            props = {}

        if "product" in props:
            kwargs["product"] = product

        for key in ("path", "core_path", "pkg_path", "package_path", "file_path", "filepath"):
            if key in props and core_path:
                kwargs[key] = core_path
                break

        # Only add license_accepted if the operator actually supports it
        # (some versions work without it, others require it but reject it in headless mode)
        for key in ("license_accepted", "accept", "confirm", "accept_warning"):
            if key in props:
                kwargs[key] = True
                break  # Use the first available acceptance parameter

        if ("install_pkt_from_file" in name) and not core_path:
            print("Skipping", name, "because KEENTOOLS_CORE_PATH is empty")
            continue

        attempted = True
        
        # Try operator call, and if it fails with license acceptance error, retry without it
        success = _call_op(op, **kwargs)
        if not success and any(k in kwargs for k in ("license_accepted", "accept", "confirm", "accept_warning")):
            print("Operator failed with license acceptance parameter, retrying without it...")
            # Remove all acceptance parameters and retry
            kwargs_no_accept = {k: v for k, v in kwargs.items() 
                              if k not in ("license_accepted", "accept", "confirm", "accept_warning", "accepted", "accept_terms", "license_agreement_accepted")}
            success = _call_op(op, **kwargs_no_accept)
        
        if success:
            try:
                bpy.ops.wm.save_userpref()
            except Exception as exc:
                print("save_userpref after core install failed:", exc)
            
            # pykeentools ne sera souvent importable qu'après redémarrage → on sort ici.
            return True

    return attempted


def _install_license() -> bool:
    """Install KeenTools license if license.ktlf exists in current directory."""
    lic_path = os.path.abspath("license.ktlf")
    
    if not os.path.exists(lic_path):
        print(f"ℹ license.ktlf not found at {lic_path}, skipping offline license install")
        return True

    op = getattr(bpy.ops.keentools_preferences, "install_license_offline", None)
    if not op:
        print("✗ install_license_offline operator not found")
        return False

    product = int(os.environ.get("KEENTOOLS_PRODUCT", "0"))
    print(f"→ Installing license from {lic_path}")
    ok = _call_op(op, product=product, filepath=lic_path)

    try:
        bpy.ops.wm.save_userpref()
    except Exception as exc:
        print("save_userpref after license install failed:", exc)

    return ok


def main() -> None:
    print("=" * 60)
    print("KeenTools CI Setup Script")
    print("=" * 60)
    
    # Step 1: Ensure addon is enabled
    print("\n[Step 1/3] Ensuring KeenTools addon is enabled...")
    _ensure_keentools_enabled()

    # Step 2: Check and install core if missing
    print("\n[Step 2/3] Checking KeenTools core (pykeentools)...")
    if _has_pykeentools():
        print("✓ pykeentools already available, skipping core install")
    else:
        print("✗ pykeentools missing, attempting to install core...")
        if _try_install_core():
            print("\n✓ Core install attempted. A Blender restart is required.")
            print("  Exit code: 77 (restart required)")
            raise SystemExit(77)
        raise SystemExit("KeenTools core install could not be started (operators missing?)")

    # Step 3: Install license if available
    print("\n[Step 3/3] Checking for offline license...")
    if not _install_license():
        raise SystemExit("KeenTools license install failed")
    
    print("\n" + "=" * 60)
    print("✓ KeenTools CI Setup completed successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
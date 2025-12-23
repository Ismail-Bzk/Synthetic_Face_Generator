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
        res = op(**clean)
        print("Result", res)
        return True
    except Exception as exc:  # pragma: no cover - Blender runtime
        print("Failed", label, exc)
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

        if ("install_pkt_from_file" in name) and not core_path:
            print("Skipping", name, "because KEENTOOLS_CORE_PATH is empty")
            continue

        attempted = True
        _call_op(op, **kwargs)

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
        print("license.ktlf not found, skipping license install")
        return True

    op = getattr(bpy.ops.keentools_preferences, "install_license_offline", None)
    if not op:
        print("install_license_offline operator not found")
        return False

    product = int(os.environ.get("KEENTOOLS_PRODUCT", "0"))
    print("Installing license from", lic_path)
    ok = _call_op(op, product=product, lic_path=lic_path)

    try:
        bpy.ops.wm.save_userpref()
    except Exception as exc:
        print("save_userpref after license install failed:", exc)

    return ok


def main() -> None:
    # 1) Make sure addon is enabled so its ops exist
    _ensure_keentools_enabled()

    # 2) If pykeentools not present, try to install core, then signal restart (77)
    if not _has_pykeentools():
        print("Attempting to install KeenTools core")
        if _try_install_core():
            print("Core install attempted. Restart Blender to load pykeentools.")
            raise SystemExit(77)
        raise SystemExit("KeenTools core install could not be started (operators missing?)")

    # 3) Core OK → install license if present
    if not _install_license():
        raise SystemExit("KeenTools license install failed")


if __name__ == "__main__":
    main()
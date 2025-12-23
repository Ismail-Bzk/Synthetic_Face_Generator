import os
import bpy


def _has_pykeentools() -> bool:
    try:
        import pykeentools  # type: ignore
    except Exception as exc:  # pragma: no cover - Blender runtime
        print("pykeentools missing:", exc)
        return False
    print("pykeentools OK:", getattr(pykeentools, "__file__", "unknown"))
    return True


def _op_label(op) -> str:
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
    if op is None:
        return False
    try:
        op.get_rna_type()
        return True
    except Exception as exc:  # pragma: no cover - Blender runtime
        print("Operator not available:", op, exc)
        return False


def _call_op(op, **kwargs) -> bool:
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


def _try_install_core() -> bool:
    ops = bpy.ops.keentools_preferences
    names = sorted(n for n in dir(ops) if "install" in n or "download" in n or "pkt" in n)
    print("KeenTools preference ops:", names)

    core_path = os.environ.get("KEENTOOLS_CORE_PATH", "").strip()
    product = int(os.environ.get("KEENTOOLS_PRODUCT", "0"))
    allow_online = os.environ.get("KEENTOOLS_ALLOW_ONLINE", "1").strip() != "0"

    candidates = []
    if allow_online:
        candidates.extend(["install_latest_pkt"])
    candidates.extend(["install_pkt_from_file", "install_pkt_from_file_with_warning"])

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
        if "install_pkt_from_file" in name and not core_path:
            print("Skipping", name, "because KEENTOOLS_CORE_PATH is empty")
            continue
        _call_op(op, **kwargs)
        if _has_pykeentools():
            return True

    return _has_pykeentools()


def _install_license() -> bool:
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
    return _call_op(op, product=product, lic_path=lic_path)


def main() -> None:
    if not _has_pykeentools():
        print("Attempting to install KeenTools core")
        if not _try_install_core():
            raise SystemExit("pykeentools still missing after install attempt")
    if not _install_license():
        raise SystemExit("KeenTools license install failed")


if __name__ == "__main__":
    main()

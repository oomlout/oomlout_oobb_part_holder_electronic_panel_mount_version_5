"""Run from the project directory with the OOBB and OOMP v5 libraries on PYTHONPATH."""
import working_oomp
import working_oomp_populate
import working_scad


def main(**kwargs):
    build_docs = kwargs.get("run_presentation", kwargs.get("generate_stl", True)
                            and {"true", "3dpr"}.issubset(kwargs.get("modes", ("true", "3dpr"))))
    part_ids = working_oomp_populate.main(**kwargs)
    kwargs["part_ids"] = part_ids
    working_oomp.main(**kwargs)
    working_scad.main(**kwargs)
    if build_docs:
        import working_presentation
        import working_navigation
        import working_verify
        working_presentation.main(**kwargs)
        working_navigation.main(**kwargs)
        working_verify.main(**kwargs)


if __name__ == "__main__":
    main()

from backend.models.model_registry import ModelRegistry
from backend.models.model_router import ModelRouter
from backend.models.model_manager import ModelManager


def main():

    print("\n==============================")
    print(" MODEL REGISTRY TEST")
    print("==============================")

    registry = ModelRegistry()

    coding = registry.get_model("coding")
    vision = registry.get_model("vision")
    general = registry.get_model("general")

    print("Coding model :", coding.name)
    print("Vision model :", vision.name)
    print("General model:", general.name)

    print("\n==============================")
    print(" MODEL ROUTER TEST")
    print("==============================")

    router = ModelRouter()

    coding_route = router.route("coding")
    vision_route = router.route("vision")

    print(
        "coding →",
        coding_route.name
    )

    print(
        "vision →",
        vision_route.name
    )

    print("\n==============================")
    print(" MODEL MANAGER TEST")
    print("==============================")

    manager = ModelManager()

    print(
        "Installed models:",
        manager.get_installed_models()
    )

    try:

        result = manager.activate(
            coding.name
        )

        print("Activation:", result)

        print(
            "Active model:",
            manager.get_active_model()
        )

    except RuntimeError as error:

        print("ERROR:", error)


if __name__ == "__main__":
    main()

    
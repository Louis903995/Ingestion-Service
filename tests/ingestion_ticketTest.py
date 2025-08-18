from app.services.tickets.ingestion_ticket import ingere_image
import base64


def encode_image(image_path: str) -> bytes | None:
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


image_path = "images/carrefour_city_1.jpg"
image_path = "images/carrefour_market_1.jpeg"
base64_image = encode_image(image_path)

resultat = ingere_image(1, base64_image)
print(resultat)

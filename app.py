
"""Flask web application for hand-sign digit recognition."""

from flask import Flask, render_template, request
from model import preprocess_img, predict_result

# Instantiating Flask app
app = Flask(__name__)


# Home route
@app.route("/")
def main():
    """Display the homepage with the image upload form."""
    return render_template("index.html")


# Prediction route
@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Process an uploaded image and display its predicted digit."""
    try:
        img = preprocess_img(request.files["file"].stream)
        pred = predict_result(img)
        return render_template("result.html", predictions=str(pred))

    except (KeyError, ValueError, OSError) as error:
        app.logger.warning("Image processing failed: %s", error)
        return render_template(
            "result.html",
            err="File cannot be processed."
        )


# Driver code
if __name__ == "__main__":
    app.run(port=9000, debug=True)

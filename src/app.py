"""
Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.

Każda akcja powoduje konieczność ,,kosztownego przeliczenia" trwającego 3 sekundy.

"""

from maindash import app
from layout import make_layout


# App layout
app.layout = make_layout()


if __name__ == "__main__":
    app.run_server(debug=True)

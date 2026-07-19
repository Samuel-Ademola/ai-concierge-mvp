from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from app.schemas.settings_schema import SettingsForm
from app.services.settings_service import save_settings

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def settings_form():
    # Minimal form (vague)
    return """
    <html>
    <body>
      <h1>Settings</h1>
      <form method="post" action="/settings/">
        <label>Hotel name: <input type="text" name="hotel_name" /></label><br/>
        <label>Contact email: <input type="email" name="contact_email" /></label><br/>
        <label>Timezone: <input type="text" name="timezone" value="UTC" /></label><br/>
        <button type="submit">Save</button>
      </form>
    </body>
    </html>
    """


@router.post("/")
async def submit_settings(hotel_name: str = Form(...), contact_email: str = Form(...), timezone: str = Form("UTC")):
    try:
        payload = {"hotel_name": hotel_name, "contact_email": contact_email, "timezone": timezone}
        form = SettingsForm(**payload)
    except ValidationError as e:
        return {"status": "error", "errors": e.errors()}

    save_settings(form.dict())
    return {"status": "saved", "data": form.dict()}

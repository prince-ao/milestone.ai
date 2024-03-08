questions = [
    """<form id="form-content">
    <ul>
        <li>
            <p>Personal Information</p>
        </li>
        <li>
            <button hx-post="/form/state" hx-trigger="click" hx-target="#form-content" hx-swap="outerHTML" hx-ext='json-enc'>next</button>
        </li>
    <ul>
</form>""",
    """<form id="form-content">
    <ul>
        <li>
            <label for="first_name">first name:</label>
            <input placeholder="first name..." type="text" id="first_name">
        </li>
        <li>
            <label for="last_name">last name:</label>
            <input placeholder="last name..." type="text" id="last_name">
        </li>
        <li>
            <button type="button">next</button>
        </li>
    </ul>
<form>"""
]

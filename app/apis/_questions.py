questions = [
    """<form id="form-content"
        hx-post="/form/state"
        hx-swap="outerHTML"
        hx-ext='json-enc'
    >
    <ul>
        <li>
            <p>Personal Information</p>
        </li>
        <li>
            <button type="submit">next</button>
        </li>
    <ul>
</form>""",
    """<form id="form-content"
        hx-post="/form/state"
        hx-swap="outerHTML"
        hx-ext="json-enc"
    >
    <ul>
        <li>
            <label for="first_name">first name:</label>
            <input
                placeholder="first name..."
                type="text"
                id="first_name"
                name="first_name"
            >
        </li>
        <li>
            <label for="last_name">last name:</label>
            <input
                placeholder="last name..."
                type="text"
                id="last_name"
                name="last_name"
            >
        </li>
        <li>
            <button type="submit">next</button>
        </li>
    </ul>
<form>"""
]

"""
Acceptance Test AT-02: Submitting without a file shows a clear error on the prediction page


opens the prediction page and clicks the "Submit" button without selecting file.

Expected:
The server does not crash.
The server responds with HTTP 200, 400 or 302 (redirect back to form).
An error message indicating the file could not be processed
"""

def test_acceptance_no_file_shows_error(client):
    """AT-02 implementation: missing file shows an error message instead of a normal prediction."""
    # Act: post to /prediction with no file in the form
    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    # Accept common behaviours: re-render form (200), bad request (400) or redirect (302)
    assert response.status_code in (200, 400, 302)

    body = response.data.lower()

    # Page should not be empty
    assert body.strip() != b""

    # App currently renders the prediction template with an error:
    # <h2 class="...">file cannot be processed.</h2>
    assert b"file cannot be processed" in body

    
  
    for digit in [b"digit 0", b"digit 1", b"digit 2", b"digit 3", b"digit 4",
                  b"digit 5", b"digit 6", b"digit 7", b"digit 8", b"digit 9"]:
        assert digit not in body


function startTest() {
    fetch('http://localhost:8000/test/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: "test_user" })
    })
    .then(response => response.json())
    .then(data => {
        alert("Test sonucu: " + data.result);
    });
}

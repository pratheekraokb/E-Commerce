document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Create a new FormData object from the form
    const formData = new FormData(this);
    for (const pair of formData.entries()) {
        console.log(pair[0], pair[1]);
    }
    console.log(tagsArray)
    const jsonObject = {
        tags: tagsArray
    };
    const jsonString = JSON.stringify(jsonObject);
    formData.append('tagsData', jsonString);
    // You can access the form data here if needed
    // For example, to get the product name: formData.get('product_name')

    // Send a POST request to the server using fetch
    fetch('{% url "create-product" %}', {
        method: 'POST',
        body: formData,
        headers: {
            // Add any headers you need, e.g., CSRF token
            'X-CSRFToken': getCSRFToken() // Assuming you have a function to get the CSRF token
        }
    })
    .then(response => response.json()) // Assuming the server responds with JSON
    .then(data => {
        // Handle the response data, e.g., show a success message or redirect
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors here, e.g., show an error message to the user
    });
});
// Function to set a cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Function to get a cookie
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

// Function to delete a cookie
function eraseCookie(name) {   
    document.cookie = name + '=; Max-Age=-99999999;';  
}

// Define an asynchronous function to get the location and update the cookie
async function updateLocation() {
    try {
        // Call getLocation() and wait for the location data
        const location = await getLocation();
        
        // Save the location data to a cookie
        setCookie("location", JSON.stringify(location), 1); // Save for a day
        
        // Log the updated location
        console.log("Location updated:", location);
    } catch (error) {
        // Handle any errors
        console.error("Error:", error.message);
    }
}

async function getLocation() {
    return new Promise((resolve, reject) => {
        // Check if the browser supports Geolocation
        if ("geolocation" in navigator) {
            // Get current position
            navigator.geolocation.getCurrentPosition(function(position) {
                // Extract latitude and longitude from the position object
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                
                // Display the coordinates
                console.log("Latitude: " + latitude + ", Longitude: " + longitude);
                
                // Resolve the Promise with the coordinates
                resolve({ "latitude": latitude, "longitude": longitude });
            });
        } else {
            // Reject the Promise if Geolocation is not supported
            reject(new Error("Geolocation is not supported by this browser."));
        }
    });
}

// Function to continuously update location in the background
// Call backgroundLocationUpdate to start updating location in the background
function backgroundLocationUpdate() {
    // Update location initially
    updateLocation();
    // Update location periodically (every hour in this example)
    setInterval(updateLocation, 60 * 20 * 1000); // 20 minutes
}


backgroundLocationUpdate();

function generateRandomCoordinates() {
    // Define latitude and longitude boundaries of Astana
    const minLatitude = 51.1;
    const maxLatitude = 51.2;
    const minLongitude = 71.3;
    const maxLongitude = 71.5;

    // Generate random latitude and longitude within the boundaries
    const latitude = Math.random() * (maxLatitude - minLatitude) + minLatitude;
    const longitude = Math.random() * (maxLongitude - minLongitude) + minLongitude;

    // Return the generated coordinates
    return { latitude: latitude, longitude: longitude };
}

// Example usage:
const randomCoordinates = generateRandomCoordinates();
console.log('Random Coordinates:', randomCoordinates);
function initMap() {
            var location = { lat: 23.8103, lng: 90.4125 }; // Dhaka, Bangladesh
            var map = new google.maps.Map(document.getElementById('map'), {
              zoom: 6,
              mapTypeId: 'roadmap',
              disableDefaultUI: true,
              styles: [
                {
                  "featureType": "all", 
                  "elementType": "geometry",
                  "stylers": [
                    { "visibility": "simplified" },
                    { "color": "#f0f0f0" }
                  ]
                }
              ],
              center: location
            });

            // Multiple locations
            var locations = [
              { lat: 23.2103, lng: 90.325, title: 'Dhaka' },
              { lat: 23.5103, lng: 90.455, title: 'Dhaka' },
              { lat: 23.1103, lng: 90.1245, title: 'Dhaka' },
              { lat: 23.9103, lng: 90.2125, title: 'Dhaka' },
              { lat: 23.8103, lng: 90.3125, title: 'Dhaka' },
              { lat: 25.4439, lng: 89.2752, title: 'Rangpur' },
              { lat: 22.1010, lng: 90.3535, title: 'Barishal' }
            ];

            locations.forEach(function(loc) {
              new google.maps.Marker({
                position: { lat: loc.lat, lng: loc.lng },
                map: map,
                title: loc.title
              });
            });
            var marker = new google.maps.Marker({
              position: location,
              map: map,
              title: 'Flood Relief Location'
            });
          }
console.log("hello from service worker");



self.addEventListener('push', function(e) {
    console.log("PUSHED DATA:");
    const data = e.data.json()
    console.log(data);
    const title = data.title
    const options = {
      body: data.body,
      data: {
        
      },
      actions: [
        {action: 'explore', title: 'Explore this new world',
          icon: 'images/checkmark.png'},
        {action: 'close', title: 'Close',
          icon: 'images/xmark.png'},
      ]
    };
    
    self.onnotificationclick = function(event) {
        console.log('event');
        console.log(event);
        
    }

    e.waitUntil(
        self.registration.showNotification(title, options)
    );
});



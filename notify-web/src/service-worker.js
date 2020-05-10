console.log("hello from service worker");



self.addEventListener('push', function(e) {
    console.log("PUSHED DATA:");
    const data = e.data.json()
    console.log(data);
    const title = data.title
    const options = {
      body: data.body,
      data: {
        href: data.href
      },
      // actions: [
      //   {action: 'explore', title: 'Explore this new world',
      //     icon: 'images/checkmark.png'},
      //   {action: 'close', title: 'Close',
      //     icon: 'images/xmark.png'},
      // ]
    };
    
    self.onnotificationclick = function(event) {
        console.log('event');
        console.log(event);
        const ntData = event.notification.data
        clients.openWindow(ntData.href)
    }
    
    e.waitUntil(
        self.registration.showNotification(title, options)
    );
});



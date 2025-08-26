# api-gifs
Dockerized API (fastapi) app to get links with random GIFs, ready to add to a website.

Avaliable to test in production at: https://api.shinpu.top

Drop in snippet to add random GIF to your website:

```javascript 
  <img id="gif" src="" alt="Random GIF">
  <br>
  <button onclick="loadRandomGIF()">Get Random GIF</button>

  <script>
    async function loadRandomGIF() {
      try {
        const response = await fetch("https://api.shinpu.top/random_gif");
        const data = await response.json();
        document.getElementById("gif").src = data.gif;
      } catch (error) {
        console.error("Error fetching GIF:", error);
      }
    }

    // Load one on page load
    loadRandomGIF();
  </script>
```

### APIdocs

1. [Home](#Home)
2. [Stream color frame](#Stream-color-frame)
3. [Stream depth frame](#Stream-depth-frame)
4. [Stream both frames](#Stream-both-frames)
5. [Manual](#Manual)
6. [Content](#Content)
7. [Emotion](#Emotion)
8. [Image](#Image)
9. [Estop](#Estop)
10. [Capture image](#Capture-image)
11. [Capture pointcloud](#Capture-pointcloud)
12. [Shutdown](#Shutdown)
13. [Get camera](#Get-camera)
14. [Face recogition](#Face-recognition)

## Home
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Home page
* **URL:** `/`
* **Method:** `GET`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `home.html`
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Check server is alive or not.
</p>
</details>

## Stream color frame
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Response color frame from depth camera
* **URL:** `/color`
* **Method:** `GET`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** `None` <br />
    **Content:** streaming color frame
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Get color frame of depth camera real-time
</p>
</details>

## Stream depth frame
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Response depth frame from depth camera
* **URL:** `/depth`
* **Method:** `GET`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** `None` <br />
    **Content:** streaming depth frame
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Get depth frame of depth camera real-time
</p>
</details>

## Stream both frames
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Response depth frame and color frame stack together
* **URL:** `/both`
* **Method:** `GET`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** `None` <br />
    **Content:** depth frame and color frame of depth camera
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Get depth frame and color frame of depth camera real-time
</p>
</details>

## Manual
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Return a GUI as manual panel for controlling
* **URL:** `/manual`
------
* **Method:** `GET`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `manual.html`
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  `estop` value in database will be readed and update in `manual.html` template as by `jinja2`
------
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
<form action = "{{ url_for('manual') }}" method = 'POST'>
  <input type = 'hidden' name = 'command' id = 'command'  value = [your-command]>
  <button class="btn btn-primary">&#8593;</button>
</form>
```
* **Success Response:**
  * **Code:** 301 <br />
    **Content:** Redirect to `manual.html`
* **Error Response:**
  * **Code:** 401 <br />
    **Content:** 401,Command Not Found
* **Sample Call:**
* **Notes:**
  `estop` value in database will be readed and update in `manual.html` template as by `jinja2`
</p>
</details>

## Content
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Update content in database
* **URL:** `/content`
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
 <form action = "{{ url_for('content') }}" method = 'POST'>
  <input class="form-control form-control-lg" type="text" placeholder = "What you wanna say?" name = "content">
  <small class="form-text text-muted">.</small>     
  <button type="submit" class="btn btn-primary mb-2">say it!</button>
</form> 
```
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** Render `manual.html` template
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  `estop` value in database will be readed and update in `manual.html` template as by `jinja2`
</p>
</details>

## Emotion
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Update Emotiton in database
* **URL:** `/emotion`
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
<form action = "{{ url_for('emotion') }}" method = 'POST'>
  <input type = 'hidden' name = 'emotion' value = '[your-emotion]'>
  <button type="submit" class="btn btn-secondary" style="font-size:50px">&#128564;</button>
</form>
```
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** Render `manual.html` template
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  `estop` value in database will be readed and update in `manual.html` template as by `jinja2`,emotion display a .gif
</p>
</details>

## Image
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Update Image in database
* **URL:** `/image`
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
<form action = "{{ url_for('image') }}" method = 'POST'>
  <input type = 'hidden' name = 'image' value = 'straightface'>
  <button type="submit" class="btn btn-secondary" style="font-size:50px">&#128528;</button>
</form>
```
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** Render `manual.html` template
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  `estop` value in database will be readed and update in `manual.html` template as by `jinja2`, image display a .png or .jpg file.
</p>
</details>

## Estop
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Update estop value in database, if estop=0 update estop=1 else udpate estop=0
* **URL:** `/estop`
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
<form action = "{{ url_for('estop') }}" method = 'POST'>
  <small class="form-text text-muted">.</small>
  <p class = 'text-center'>
      {% if estop == True %}
          <button type="Estop" class="btn btn-danger mb-4">ESTOP</button>
      {% else %}
          <button type="Estop" class="btn btn-primary mb-6">ESTOP</button>
      {% endif %}
  </p>
</form>
```
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** Render `manual.html` template
  * **Code:** 201 <br />
    **Content:** Render `manual.html` template
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Color of estop button will change, blue if estop=0 red if estop=1
</p>
</details>

## Capture image
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Capture current frame of robot's camera
* **URL:** `/capture_img`
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
<form action = "{{ url_for('capture_img') }}" method = 'POST'>
    <input type = 'hidden' name = 'capture image'>
    <button class="btn btn-primary mb-2">cap img</button>
</form>
```
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** Render `manual.html` template
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  `estop` value in database will be readed and update in `manual.html` template as by `jinja2`
</p>
</details>

## Capture pointcloud
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Capture current pointcloud (depth-frame) of robot's camera
* **URL:** `/capture_pointcloud`
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
<form action = "{{ url_for('capture_pointcloud') }}" method = 'POST'>
  <input type = 'hidden' name = 'capture pointcloud'>
  <button class="btn btn-primary mb-2">cap pointcloud</button>
</form>
```
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** Render `manual.html` template
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  `estop` value in database will be readed and update in `manual.html` template as by `jinja2`
</p>
</details>

## Shutdown
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Shutdown robot's local flask server
* **URL:** `/shutdown`
* **Method:** `POST`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Web Form:**
```
<form action = "{{ url_for('shutdown') }}" method = 'POST'>
  <button class="btn btn-danger mb-2">shutdown server</button>
</form>
```
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** 'Server shutting down'
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:** `None`
</p>
</details>

## Get camera
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Response serial-camera frame
* **URL:** `/camera`
* **Method:** `GET`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** `None` <br />
    **Content:** streaming frame of serial-camera
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Get color `RGB` frame of serial-camera real-time, function's name in `routes.py` `get_cam`
</p>
</details>

## Face recognition
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Response face-recognition detected by serial-camera
* **URL:** `/face`
* **Method:** `GET`
*  **URL Params:**
   **Required:**`None`
   **Optional:**`None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** `None` <br />
    **Content:** streaming detected face on frame of serial-camera
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  face-recognition application, function's name in `routes.py` `get_face`
</p>
</details>
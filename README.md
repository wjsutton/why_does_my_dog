<h1 style="font-weight:normal"> 
Why Does My Dog... :dog2: :poodle: :service_dog:
</h1>

A data visualisation of the rather odd habits of dogs.
<br>

[![Status](https://img.shields.io/badge/status-active-success.svg)]() [![GitHub Issues](https://img.shields.io/github/issues/wjsutton/why_does_my_dog.svg)](https://github.com/wjsutton/why_does_my_dog/issues) [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/wjsutton/why_does_my_dog.svg)](https://github.com/wjsutton/why_does_my_dog/pulls) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)<br>


<br>

<!--/div-->

<!--
Quick Link 
-->

[Twitter]:https://twitter.com/WJSutton12
[LinkedIn]:https://www.linkedin.com/in/will-sutton-14711627/
[GitHub]:https://github.com/wjsutton
[Website]:https://wjsutton.github.io/

<table border="0">
 <tr>
    <td><b>:rocket: PROJECT</b></td>
    <td><b>:link: LINK</b></td>
 </tr>
 <tr>
    <td><a href="https://sarahlovesdata.co.uk/2023/02/26/iron-quest-weird-or-wonderful-recap/">Iron Quest</a></td>
    <td><a href="https://public.tableau.com/app/profile/wjsutton/viz/WhyDoesMyDog___IronQuest/DesktopVersion">Tableau Public</a></td>
 </tr>
 <tr>
    <td><b>:hammer_and_wrench: TOOLS</b></td>
    <td><b>:oil_drum: DATA</b></td>
 </tr>
 <tr>
    <td>Python, R, <br>Tableau Public, <br>Figma</td>
    <td>List of dog breeds, <br>Google suggestions API, <br>and radial heatmap generator<a href="https://github.com/wjsutton/radial_heatmap_generator"></a></td>
 </tr>
 <tr>
    <td><b>:trophy: AWARDS</b></td>
    <td><b>:newspaper: CITATIONS</b></td>
 </tr>
 <tr>
    <td><a href="https://public.tableau.com/app/discover/viz-of-the-day">Viz of the Day 2023-01-12</a><br><a href="https://public.tableau.com/app/profile/wjsutton/viz/WhyDoesMyDog___IronQuest/DesktopVersion">150+ :star: on Tableau Public</a></td>
    <td></td>
 </tr>
</table>


### :a: About

Dogs are amazing, man’s best friend you might say! But for any dog owners, you’ll know that they come with some unusual habits, like snoring, excessive farting and howling in their sleep. 

To find out which breeds have the strangest habits I’ve consulted Google Search’s Autocomplete feature and retrieved data on 60 popular dog breeds to find our most common questions.


<div style="overflow: hidden;margin: 0 10px 0 0">
<a href="https://public.tableau.com/app/profile/wjsutton/viz/WhyDoesMyDog___IronQuest/DesktopVersion">
<img src='https://github.com/wjsutton/why_does_my_dog/blob/main/design/Dash.png?raw=true' width="100%">
</a>
</div>

<h1 style="font-weight:normal"> 
:hammer: Building the Visualisation
</h1>


### :oil_drum: Data Sources

- [List of dog breeds](https://github.com/wjsutton/why_does_my_dog/blob/main/data/dog_breeds.csv) modified from [wjsutton/the_kennel_club](https://github.com/wjsutton/the_kennel_club) with a few additional dog breeds
- [Google suggestions API](https://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=why+does+my+dog) a largely undocumented API of the form `https://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=YOUR+QUERY` returns an XML output
- [Radial Heatmap Generator](https://github.com/wjsutton/radial_heatmap_generator) an R Shiny app to generate a radial heatmap to plot points

### :white_circle: Data Reshape

- [get_google_dog_suggestions.py](https://github.com/wjsutton/why_does_my_dog/blob/main/get_google_dog_suggestions.py) feeds [List of dog breeds](https://github.com/wjsutton/why_does_my_dog/blob/main/data/dog_breeds.csv) into the [Google suggestions API](https://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=why+does+my+dog) and returns a dataset of all search queries related to different dog breeds.
- [data_prep.py](https://github.com/wjsutton/why_does_my_dog/blob/main/data_prep.py) cleans up the suggested queries into reasonable groups, e.g. smell, stinks, smells so bad, and removes queries that aren't related to dogs, e.g. "why does my boxers ride up" to form the output [dashboard_data/why_does_my_dog.csv](https://github.com/wjsutton/why_does_my_dog/blob/main/dashboard_data/why_does_my_dog.csv)
- [sunburst_gen.R](https://github.com/wjsutton/why_does_my_dog/blob/main/sunburst_gen.R) is an early version of [wjsutton/radial_heatmap_generator](https://github.com/wjsutton/radial_heatmap_generator) that creates the points of a radial heatmap to join to the dataset, [dashboard_data/test_sunburst.csv](https://github.com/wjsutton/why_does_my_dog/blob/main/dashboard_data/test_sunburst.csv)

### :a: Visual Alphabet and Accessibility

The aim for this viz was to create a static eye-catching design to draw readers in, that would one day be published. 

Accessibility was comprimised to make the work more engaging, for example:

- Radial charts are harder to read and size data different depending on its position towards the inner/outer ring
- The colour palette isn't colourblind friendly
- All text is contained in an image background so won't be picked up by a screen reader

After sacrifing accessibility to get my readers attention I needed to make the data easy to interpret. To do this I've answered the basic questions with notes on the dashboard. 

e.g. the first note "Why does my French Bulldog fart so much?" introduces the reader to

- What the segments in the radial are
- What the colours mean
- The context and humour associated with the viz


### :chart_with_upwards_trend: Charting in Tableau

The visualisation utilises the map layers function in Tableau to convert the X, Y co-ordinates into latitude, longitude, and allows me to stack multiple datapoints on top of each other. This helps with the labelling of the segments. 

### :framed_picture: Figma Background

The background of this visualisation was created in Figma:

- Title Font: Luckiest Guy
- All other text: BentonSans Regular (same as Tableau Regular)

<img src='https://github.com/wjsutton/why_does_my_dog/blob/main/design/Dash_Background.png?raw=true' width="80%">
---

<div style="overflow: hidden;margin: 0 10px 0 0">
<a href="https://public.tableau.com/app/profile/wjsutton/viz/WhyDoesMyDog___IronQuest/DesktopVersion">
<img src='https://github.com/wjsutton/why_does_my_dog/blob/main/design/Dash.png?raw=true' width="100%">
</a>
</div>

Will Sutton, March 2023<br>
[Twitter][Twitter] :speech_balloon:&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[LinkedIn][LinkedIn] :necktie:&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[GitHub :octocat:][GitHub]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Website][Website] :link:

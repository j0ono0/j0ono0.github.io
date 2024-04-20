title:   Some more thoughts
authors: j0ono0
created:    2024-4-16
updated:   2024-4-17

Just another markdown doc. to see how content might be filed and used.

Things not immediately obvious include the use of Markdown Meta-data. It is included at the top of each markdown content page and makes for a handy way to include some meta data with the content. 

It might become painful pattern for image heavy content? I could potentially have a .md file for every media item. 

Maybe that wouldn't be so bad. The file could include:

- src
- title
- description (long and short?)
- alt text
- related thumbnail(s)
- image-set alternatives
- size alternatives

other thoughts...

- how to handle css.
  - concatinate it all together
  - copy into the build folder and link to there (*this is what is currently happening*)

- Validating that data is correct as much as possible when generating!!! I've gotten site nav and links wrong several times already with just 3 and 4 pages.
- Markdown is nice, but I could also support .rst?
- Thinking about overriding some Markdown but feel like it's a bad idea to mess with expected output from it.
  My motive is the desire to  support some more html tags with 'short-hand' markup. Specifically using image-set to serve webp images and jpg/png fallback.
- Related to above - auto-processing images to useful formats. eg creating thumbnails and webp versions (even image-sets) for a gallery component.
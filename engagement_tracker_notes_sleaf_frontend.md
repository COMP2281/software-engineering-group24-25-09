# Notes on Engagement Tracker UI (Frontend)

"Content" will be the preview of each slides we made.

**The search bar searches, but it doesn't search yet, because we haven't made it search for anything that needs to be searched. But we'll make it search because searching for things that need to be searched is important because some searchable data cannot be accessed without searching, and so we search for information and output the searched information.**

If you click on the moon, it turns into a sun and light mode is enabled! Click the sun and it turns back into a moon and dark mode is back!

### New Slide button

Clicking on "New Slide" gets you a window allowing you to select something. Each of these selections will be names of engagements with the date!

My assignment: add a filter to search by date. And let the search bar work so we can search for searchable engagements that match for things that we want to search and also search for things that are close to being searched.

For example, the engagement title may be ["IBM engagment with Durham Uni", "2025-01-21"]. We need to extract the equivalent of "2025-01-21" and calculate the difference between the given date and the engagements. 

We could also allow the end-user to search for a month or year of engagements. Let's highlight exact dates, and then get non-exact dates under a "Didn't find what you were looking for? Try these" section.

### Problems found

I've noticed that the engagement tracker window can't be dragged. Is this intentional or do we want to fix it?
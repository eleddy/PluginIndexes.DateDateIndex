
Introduction
============

This is a Date Index. If you care about time, then turn around. If you care about 
timezones, turn around. If however you only wish for the utter humiliating 
destruction of timezones, then you have come to the right place.

Motivation
----------
The best way to describe this is to think about the use case(cover your eyes if you 
don't like dirty words): reports.

The core case for this is events/meetings/appointments/etc. Sure you care about 
time if you are displaying details but when reporting its about as useful as a monkey 
on a pogo stick. Here you want to do queries such as "show me how many appointments I 
had on May 08 2011." The query for that with the current DateTime catalog looks 
something like:: 

  ...
  {'query':DateTime('2011-05-08',
           DateTime('2011-05-08')+.999999999),
    'range': 'min:max'}},
  ...
  
Without the .99999 a bunch of stuff gets filtered. Oh, and if your portal is in a 
different timezone than the server running it, forget about getting anything consistent.

Furthermore, we can send in just about any data you want and convert it. You like strings?
We got strings. You like datetime? We got datetime. Oh, and it takes care of that pesky 
"/" vs "-" thing as well when parsing strings.

Of course, with careful code planning an monitoring we can avoid all this but who has 
time for that. Enter DateDateIndex. DateDateIndex is the counter to DateTimeIndex, which 
coincidentally was renamed to DateIndex, although it is actually a DateTime Index. 

The Details
-----------
This index will take a date, time, datetime, DateTime, or string. It will discard 
any time and timezone information faster than you can say uncle. Then it will turn 
it into a time neutral DateTime object and store like any other. The difference 
being that you can query and not have to worry about timezones, since it will always 
be native to the local server.

To use, simply add a new DateDateIndex from the ZMI like you would any other. When you 
query, you can also query like you would, except its very flexible. The scenario above 
would look more like::

  ...
  {'query':'2011-05-08',
           '2011-05-08'),
    'range': 'min:max'}},
  ...
  
If you send in times for the query they will get stripped too. Query can also take any 
meaningful data type like DateTime, datetime, etc...

Note that the current version has only been tested on Plone 4.x. Who knows what lies in 
store for the rest.
  
Thoughts
--------
 - Has this been extensively tested? Nope. 
 - Are there better ways to do this? Probably, but this seemed the fastest way at the moment. 
 - What is the performance like? No idea. Although this inherits from DateIndex so all those 
optimizations will trickle down. 
 - Is this a good solution for me? Probably not. This is currently being tested before hitting 
   a live site and is without issues but tread carefully. It's not SO insance.
 - Only tested in Plone 4.0 and 4.1

Bugs/Questions/Whatever
-----------------------
https://github.com/eleddy/PluginIndexes.DateDateIndex


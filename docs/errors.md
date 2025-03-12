# Troubleshooting program errors

## Frontend errors

### "All scraping credits have been used for today"

[Todo: An image of the error message]

If you get an error message of or similar to:

> All scraping credits have been used for today. Please try again tomorrow.

when attempting to scrape new web engagements, this means that you have used all of your credits for the Google Search API for the day. This error message may be caused by using the web scraper too frequently. 

To solve this error, you will need to wait until tomorrow before you can use the web scraper again.

## Internal error logs

### Pickle, EOF, recursion or import error

Sometimes, serial data files may be corrupted. You may get an error message mentioning one of the above.

To solve such an error, enter the data folder and try to delete the serial data files to reset them:

- `pages.pickle` contains cached webpages
- `engagements.pickle` contains engagement objects

Note that you will lose your engagements if you delete the `engagements.pickle` file.

## Setup script errors

### Python not found, please enter the correct path

If you get an error message of or similar to:

> Python 3.13 not found; Please enter the correct Python path.

when setting up the program, this mean that the script could not find your Python installation on its own.

To solve this error, you can enter the path to your Python executable. If you added your executable to the PATH variable, then you may need to restart your computer for the changes to take effect.

### Python.exe not found

If you get an error message of or similar to:

>../python.exe not found.

when setting up the program, this means that the Python executable you provided could not be found.

To solve this error, please make sure that the path to the Python executable you gave is correct, and ensure that there is no leading or trailing whitespace.

### Python.exe has version x.y.z

If you get an error message of or similar to:

>../python.exe has version x.y.z.

when setting up the program, where x, y and z are numbers, this means that the Python executable you provided is not of Python version 3.13.

To solve this error, please make sure that the path to the Python executable you gave corresponds to an executable of version 3.13.
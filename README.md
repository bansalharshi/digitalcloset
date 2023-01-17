# My Closet
#### Video Demo:  <https://www.youtube.com/watch?v=s4tZAkEeReE>
#### Description:

## Problem statement
Many of us buy clothes online. As we continue to buy clothes online and tuck them away in our physical closets its easy to forget the amount of clothes we own and how much money we already spend on it on a regular basis. When we buy clothes online, its also tedious to keep looking for the clothes we own to find new clothes to style with. For example, if we own a pair of nice jeans we might be able to create different looks using the tops, jackets, accessories, etc. we pair it with. But, finding this pair of jeans everytime we buy something new online can be a problem.

## Features
So, it would be nice to have a digital closet where we can store all the clothes we buy to reference it when we buy new clothes online, to remind us of the money we have spent and style outfits for any ocassion. In this project we build a digital closet. It lets you:
1. Create an account
2. Log in to an existing account
3. Add clothes (or any other item in your wardrobe) with as much information as you want including name, price, brand, pictures, original product link.
4. Display added items in the form of your own personal closet on the web along with name, brand, image, any notes and a link to the original shopping page. Using the link to the original shopping page you can go back to the website for any styling ideas.
5. Filter added items based on 3 main categories of clothes, accessories and shoes
6. Keep track of the amount of money spent on buying clothes by displaying a list of all the items along with price and total

## Backend
In the backend I use the flask framework inspired by the CS50Finance project. There 2 python files app.py and helpers.py. app.py contains the control functions and helpers.py contains functions which are used across all control functions. All the HTML files are stored in templates folder. The static folder contains the images used across various webpages in the webapp. I store all the information in 2 tables: users and items. users table contains the user_id and password for each account. items table contains all the information entered by the user related to each item.

## Future vision
Currently, the most tedious part of maintaining the closet is adding each item and its every detail manually. In the future, this can be made easier by allowing users to scan receipts or fetching the data directly from the original shopping page using scrapping APIs.

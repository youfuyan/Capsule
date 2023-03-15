# Module 1 Group Assignment

CSCI 5117, Spring 2023, [assignment description](https://canvas.umn.edu/courses/355584/pages/project-1)

## App Info:

This is dev branch.

- Team Name: Capsule
- App Name: Capsule

- App Link (deploy on main branch):

https://capsule-igtc.onrender.com

### Students

- Youfu Yan, yan00111@umn.edu
- Isabel Dahl, dahl1199@umn.edu
- Marcellinus, Steven Sugiarto sugia005@umn.edu
- Ying Lu, lu000097@umn.edu
- Ola Oladeji, olade014@umn.edu

## Key Features

**Describe the most challenging features you implemented
(one sentence per bullet, maximum 4 bullets):**

- Applied a decorator to restrict some actions (such as commenting or liking) for users who are not logged in.
- Implemented full text search and fuzzy search to allow users to find photos based on their captions or descriptions.
- Realized Responsive design that makes web pages render well on different devices and screen sizes and adaptable to mobile devices.
- Implemented comment and like system to enable real-time communication and feedback among users without reloading the page.

## Testing Notes

**Is there anything special we need to know in order to effectively test your app? (optional):**
Here are suggestions for testing:

1. Click the 'exploring' button on the landing page to see the gallery
2. Without logging in, click any post to see the comments page
3. Without logging in, click the like button or comment button to redirect to the landing page
4. Without logging in, click the search button to search for posts by keywords or hashtags
5. Without logging in, click the 'add new post' button to redirect to the landing page
6. Click the 'login' button on the landing page to login
7. After logging, click the 'add new post' button to add a new post
8. After logging, click the 'search' button to search for posts by keywords or hashtags
9. After logging, click the 'like' button to like a post
10. After logging, click the 'comment' button to comment on a post
11. After logging, click the 'profile' button to see the profile page
12. On the profile page, click the 'edit profile' button to edit the profile and click the 'save' button to save the changes
13. On the edit profile page, click the 'delete' button to delete a post
14. Click the 'logout' button to logout and redirect to the landing page

## Screenshots of Site

**[Add a screenshot of each key page (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository)
along with a very brief caption:**

### Gallery

![Gallery](./Demo/1.png 'Gallery')

### Search

![Search](./Demo/2.png 'Search')

### Add new post

![Add new post](./Demo/3.png 'Add new post')

### Comments

![Comments](./Demo/4.png 'Comments')

### Profile

![Profile](./Demo/5.png 'Profile')

## External Dependencies

**Document integrations with 3rd Party code or services here.
Please do not document required libraries. or libraries that are mentioned in the product requirements**

- Web Hosting: [Render](https://render.com/)
- Database: [PostgreSQL on Render](https://render.com/docs/postgres)
- Photo Storage: [Imagekit](https://imagekit.io/)
- Authentication: [Auth0](https://auth0.com/)

**If there's anything else you would like to disclose about how your project
relied on external code, expertise, or anything else, please disclose that
here:**
None

# Legacy

## Mock-up

There are a few tools for mock-ups. Paper prototypes (low-tech, but effective and cheap), Digital picture edition software (gimp / photoshop / etc.), or dedicated tools like moqups.com (I'm calling out moqups here in particular since it seems to strike the best balance between "easy-to-use" and "wants your money" -- the free teir isn't perfect, but it should be sufficient for our needs with a little "creative layout" to get around the page-limit)

In this space please either provide images (around 4) showing your prototypes, OR, a link to an online hosted mock-up tool like moqups.com

https://www.figma.com/file/t4tzlTlzw1cuJrDizenWRE/Capsule-Prototype?node-id=0%3A1&t=Ao2MbAzyLNCByPPH-1

### Preview

![](./Mockups/1.png 'Adding new post')
![](./Mockups/2.png 'Searching')
![](./Mockups/3.png 'Gallery')
![](./Mockups/4.png 'Comments')

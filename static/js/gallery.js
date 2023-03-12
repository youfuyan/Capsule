
const post = document.querySelectorAll('.post');

console.log(post)


async function handleGetCommentsNum(photoId){
  try{
      let fetchURL = "/api/comments/get/photo/" + photoId;
      let res = await fetch(fetchURL, {
          method: 'GET'
      });
      return res.json();
  }
  catch(error){
      return "Error";
  }
}
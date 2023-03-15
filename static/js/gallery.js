async function handleAddLike(provider, userId, photoId) {
    console.log(arguments);
    try{
        let fetchURL = "/api/likes/create/" + provider + "/" + userId + "/" + photoId;
        let res = await fetch(fetchURL, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_id: userId, photo_id: photoId})
        });
        return res.json();
    }
    catch(error){
        return "Error";
    }
}

async function handleRemoveLike(provider, userId, photoId){
    try{
        let fetchURL = "/api/likes/delete/" + provider + "/" + userId + "/" + photoId;
        let res = await fetch(fetchURL, {
            method: 'DELETE'
        });
        return res.json();
    }
    catch(error){
        return "Error";
    }
}

async function handleGetLikesUser(provider, userId){
    try{
        let fetchURL = "/api/likes/get/user/" + provider + "/" + userId;
        let res = await fetch(fetchURL, {
            method: 'GET'
        });
        return res.json();
    }
    catch(error){
        return "Error";
    }
}

async function handleGetLikesPhoto(photoId){
    try{
        let fetchURL = "/api/likes/get/photo/" + photoId;
        let res = await fetch(fetchURL, {
            method: 'GET'
        });
        return res.json();
    }
    catch(error){
        return "Error";
    }
}

function likeFunctionality(){
    document.querySelectorAll('.like-button').forEach(button =>{
        button.addEventListener('click', (e) => {
            let id = e.target.id;
            let index = id.split('-')[2];
            
            let postClassName = "post-" + index;

            let photo = document.getElementsByClassName(postClassName)[0];
            let photoId = photo.id;

            let userIdRaw = document.getElementsByClassName("owner-id-gallery-page")[0].id;
            let provider = userIdRaw.split("|")[0];
            let userId = userIdRaw.split("|")[1];
            
            handleAddLike(provider, userId, photoId).then((status) =>{
                console.log(status);
                if(!status.success){
                    handleRemoveLike(provider, userId, photoId).then(() => photo.querySelector(".like-button").classList.remove("is-liked"));
                    
                }
                personalLikesCheck();
                generalLikesCheck();
            });
    
        })
    })
}

function personalLikesCheck(){
    let userIdRaw = document.getElementsByClassName("owner-id-gallery-page")[0].id;
    let provider = userIdRaw.split("|")[0];
    let userId = userIdRaw.split("|")[1];
    
    handleGetLikesUser(provider, userId).then((likes) => {
        if (likes.length > 0){
            likes.forEach((like) => {
                let photoElement = document.getElementById(like.photo_id);
                let likeElement = photoElement.querySelector(".like-button");
                
                likeElement.classList.add("is-liked")
            })
        }
    });
    
    
}

function generalLikesCheck(){
    let posts = document.querySelectorAll(".post-icons");
    posts.forEach((post) => {
        photoId = post.id;

        handleGetLikesPhoto(photoId).then((data) => {
            let likeElement = post.querySelector('#like-num');
            // let likeElement = post.querySelector(".like-number");
            likeElement.innerHTML = data.length;
        })
    })
    
}


async function handleGetCommentsPhoto(photoId){
  try{
      let fetchURL = "/api/comments/get/" + photoId;
      let res = await fetch(fetchURL, {
          method: 'GET'
      });
      return res.json();
  }
  catch(error){
      return "Error";
  }
}

function handleCommentNumber() {
  let posts = document.querySelectorAll(".post-icons");
    posts.forEach((post) => {
        photoId = post.id;

        handleGetCommentsPhoto(photoId).then((data) => {
            // let commentElement = post.querySelector(".comment-number");
            let commentElement = post.querySelector("#comment-num");
            commentElement.innerHTML = data.length;
        })
    })
}

function main(){
    // for changing like color based on whether the user liked or not
    personalLikesCheck();

    // for checking the like numbers of each photos
    generalLikesCheck();

    // listener to like or not like and store them
    likeFunctionality();

    // for checking the comment numbers of each photos
    handleCommentNumber();
}

main();

async function handleAddLike(userId, photoId){
    try{
        let res = await fetch("/api/likes/create", {
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

async function handleRemoveLike(userId, photoId){
    try{
        let fetchURL = "/api/likes/delete/" + userId + "/" + photoId;
        let res = await fetch(fetchURL, {
            method: 'DELETE'
        });
        return res.json();
    }
    catch(error){
        return "Error";
    }
}

async function handleGetLikesUser(userId){
    try{
        let fetchURL = "/api/likes/get/user/" + userId;
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

async function handleCheckLike(userId, photoId){
    try{
        let res = await fetch("/api/likes/create", {
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

function likeFunctionality(){
    document.querySelectorAll('.like-button').forEach(button =>{
        button.addEventListener('click', (e) => {
            let id = e.target.id;
            let index = id.split('-')[2];
            
            let postClassName = "post-" + index;

            let photo = document.getElementsByClassName(postClassName)[0];
            let photoId = photo.id;

            let userIdRaw = document.getElementsByClassName("owner-id-gallery-page")[0].id;
            
            if(photo.querySelector(".like-button").classList.contains("is-liked")){
                let userId = userIdRaw.split("|")[1];
                handleRemoveLike(userId, photoId).then();
                photo.querySelector(".like-button").classList.remove("is-liked");
            } else{
                handleAddLike(userIdRaw, photoId).then();
            }
            personalLikesCheck();
            generalLikesCheck();
    
        })
    })
}

function personalLikesCheck(){
    let userIdRaw = document.getElementsByClassName("owner-id-gallery-page")[0].id;
    let userId = userIdRaw.split("|")[1];
    
    handleGetLikesUser(userId).then((likes) => {
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
    let posts = document.querySelectorAll(".post");
    posts.forEach((post) => {
        photoId = post.id;

        handleGetLikesPhoto(photoId).then((data) => {
            let likeElement = post.querySelector(".like-number");
            likeElement.innerHTML = data.length;
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
}

main();

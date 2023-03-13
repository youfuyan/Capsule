async function handleGetCommentsName(userId){
  try{
      let fetchURL = "/api/users/get" + userId;
      let res = await fetch(fetchURL, {
          method: 'GET'
      });
      return res.json();
  }
  catch(error){
      return "Error";
  }
}

function handleCommentName(comment) {
    let userId = comment["user_id"];
    let username = handleGetCommentsName(userId)["username"];
    document.getElementById("comment-name").innerHTML = username;
}

function main(){

  // for rendering the comment username
  handleCommentName();
}

main();

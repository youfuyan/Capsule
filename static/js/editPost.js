async function handleDeletePost(photoId){
    try{
        let fetchURL = "/deletePost";
        let res = await fetch(fetchURL, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({photo_id: photoId})
        });
        return res.json();
    }
    catch(error){
        return "Error";
    }
}

function main(){
    document.getElementById("delete-button").addEventListener("click", (e) => {
        let confirmation = confirm("Are you sure want to delete this?")
        console.log(confirmation);
        if(confirmation){
            document.getElementById("delete-post-form").submit();
        }
    })
}

main();



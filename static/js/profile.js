// document.querySelectorAll('.profile-img').forEach(((element) =>{
//     element.addEventListener('mouseover', (e) => {
//         // console.log(e.target.id)
//         let boxId = e.target.id;
//         // console.log(boxId);
//         let buttonId = "button-" + boxId;
//         console.log("in");
//         if(document.getElementById(buttonId).classList.contains("hidden-post")){
//             document.getElementById(buttonId).classList.remove("hidden-post");
//         }
//     })

//     element.addEventListener('mouseleave', (e) => {
//         let boxId = e.target.id;
//         let buttonId = "button-" + boxId;
//         if(!document.getElementById(buttonId).classList.contains("hidden-post")){
//             document.getElementById(buttonId).classList.add("hidden-post");
//         }
//         // document.getElementById(buttonId).classList.add("hidden");
//         console.log("out");
//     })


// }))

// document.querySelectorAll('.edit-post').forEach(((element) =>{
//     element.addEventListener('mouseover', (e) => {
//         // console.log(e.target.id)
//         let boxId = e.target.id;
//         // console.log(boxId);
//         let buttonId = "button-" + boxId;
//         console.log("in-post");
//         if(document.getElementById(buttonId).classList.contains("hidden-post")){
//             document.getElementById(buttonId).classList.remove("hidden-post");
//         }
//     })

//     element.addEventListener('mouseleave', (e) => {
//         let boxId = e.target.id;
//         let buttonId = "button-" + boxId;
//         if(!document.getElementById(buttonId).classList.contains("hidden-post")){
//             document.getElementById(buttonId).classList.add("hidden-post");
//         }
//         // document.getElementById(buttonId).classList.add("hidden");
//         console.log("out-post");
//     })


// }))


function editButton() {
    document.getElementById("edit-form").submit();
}

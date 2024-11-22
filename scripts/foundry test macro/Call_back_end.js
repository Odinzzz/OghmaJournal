fetch("https://172.31.112.1:5000/test").then(response => response.json()).then(data => {

    console.log(data.content);
    
})
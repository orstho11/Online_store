const searchBlock = document.querySelector('#searchBlock');

const tableSearchOutput = document.querySelector(".tableSearchOutput");
const tableIndex = document.querySelector(".indexTable");
const pagination = document.querySelector(".pagination");
const tableBody = document.querySelector(".tableBody");
tableSearchOutput.style.display = "none";


searchBlock.addEventListener("keyup", (e) => {
    const  searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        pagination.style.display = 'none';
        tableBody.innerHTML = '';


        fetch("/product/search", {
            body: JSON.stringify({searchQuery: searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {

                tableIndex.style.display = "none";
                tableSearchOutput.style.display = "block";

                if (data.length === 0) {
                    tableSearchOutput.innerHTML = "No results found";
                }else {
                    data.forEach((item) =>{
                        tableBody.innerHTML +=`
                            <tr>
                                <td > <a href="/product/${item.id}/detail" >${item.name}</a></td>
                                <td >${item.description}</td>
                                <td >${item.amount}</td>
                                <td >${item.price}</td>
                            </tr>
                            `;
                    });



                }
            });

    }else {
        tableSearchOutput.style.display = "none";
        tableIndex.style.display = "block";
        pagination.style.display = 'block';
    }
})
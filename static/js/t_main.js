// main.js
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    // 假设你的搜索API地址为 '/api/search'
    async function searchHeritage(query) {
        const response = await fetch(`search?q=${encodeURIComponent(query)}`);
        const heritageList = await response.json();
        return heritageList;
    }

    searchInput.addEventListener('input', async function (event) {
        const searchText = event.target.value.toLowerCase();
        if (!searchText) {
            searchResults.innerHTML = '';
            return;
        }

        const heritageData = await searchHeritage(searchText);

        displaySearchResults(heritageData);
    });

    async function handleSearchInput(event) {
    const searchText = event.target.value;
    const response = await searchHeritage(searchText);
    if (response.ok) {
        const results = await response.json();
        if (Array.isArray(results)) {
            displaySearchResults(results);
        } else {
            console.error('Response is not an array:', results);
        }
    } else {
        console.error('Error fetching search results:', response.statusText);
    }
}

    function displaySearchResults(results) {
        searchResults.innerHTML = '';



        results.forEach(item => {
            const resultItem = document.createElement('div');
            resultItem.innerHTML = `
                <h5>大类：${item.category}</h5>
                <h4>非遗项目：${item.project_name}</h4>
                <p>简述：${item.description}</p>
            `;
            searchResults.appendChild(resultItem);
        });
    }
});
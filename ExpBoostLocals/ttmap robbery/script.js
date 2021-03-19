const domImg = document.getElementById("mapImg");
const domCanvas = document.getElementById("mapCanvas");
const ctx = domCanvas.getContext("2d");
const domDotList = document.getElementById("dotList");
const domPlayerCard = document.getElementById("playerCard");
const domSidebar = document.getElementById("sidebar");
const domMapOptions = createSidebarBlock("Map Options", false);
const domToggleSidebarButton = document.getElementById("toggleSidebar");
// const playersCount = document.getElementById("playersCount");
// const errors = document.getElementById("errors");

const playersData = {};
const permanentJobsList = {};
const temporaryPlayersList = {};
const activeFilterJobsList = [];
const activeFilterPlayersList = [];

const mapOptions = {
    list: [
        ["Dark Map", "https://supernovaplus.github.io/ttmap/images/maps/mapdarkmobile.jpg"],
        ["Color Map", "https://supernovaplus.github.io/ttmap/images/maps/mobilemap.jpg"]
    ],
    selected: 0
}
let activeTimeout = null;
const updateTime = 6000;


//first find the zero position, then scale the image
const imageSize = { width: 2304, height: 2304 };
const map_center_x = (imageSize.width * 0.5) - 53;
const map_center_y = (imageSize.height * 0.5) + 346;
const scale = 6.05;
domCanvas.width = imageSize.width;
domCanvas.height = imageSize.height;

domSidebar.style.maxHeight = window.innerHeight - 50 + "px";
window.addEventListener("resize", ()=>{
    domSidebar.style.maxHeight = window.innerHeight - 50 + "px";
});

//Toggle Options Button
(()=>{
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = true;

    domToggleSidebarButton.prepend(checkbox);

    toggleElementDisplay(domSidebar)
    toggleElementDisplay(domToggleSidebarButton)
    domToggleSidebarButton.onclick = () => toggleSidebar(checkbox, domSidebar);
})();

//Map Options Block
(()=>{
    //map selection
    const row1 = document.createElement("div");
    row1.className = "row";

    const firstTitle = document.createElement("p");
    firstTitle.innerText = "Select Map:";
    row1.appendChild(firstTitle);

    mapOptions.list.forEach(_map => {
        const mapSelectBtn = document.createElement("input");
        mapSelectBtn.type = "button";
        mapSelectBtn.value = _map[0];
        mapSelectBtn.onclick = () => {
            domImg.src = _map[1];
        }

        row1.appendChild(mapSelectBtn);
    })
    domMapOptions.appendChild(row1);
})();


//========================
domImg.onload = ()=>{
    console.log("image loaded");
    window.scrollTo(0, domImg.width * 0.5);
    domImg.onload = null;
}



function getDistance(position1, position2){
    return Math.abs(position1[0] - position2[0]) + Math.abs(position1[1] - position2[1]);
}



function newRowCheckbox(target, value, onchange){
    const rowElement = document.createElement("div");
    rowElement.className = "row";

    const inputRadio = document.createElement("input");
    inputRadio.type = "checkbox";
    inputRadio.value = value;
    inputRadio.onchange = onchange;

    const inputText = document.createElement("p");
    inputText.innerText = value;

    rowElement.appendChild(inputRadio);
    rowElement.appendChild(inputText);
    target.appendChild(rowElement);

    return inputRadio;
}



function coordsToMap(_x, _y){
    return [(_x / scale) + map_center_x, (_y / -scale) + map_center_y];
}

const color_letters = '0123456789ABCDEF';
function getRandomColor() { //https://stackoverflow.com/a/1484514/9601483
    let color = '#';
    for (let i = 0; i < 6; i++) { color += color_letters[Math.floor(Math.random() * 16)]; }
    return color;
}

function createSidebarBlock(text, enabled = true){
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = true;

    const block = document.createElement("div");
    block.className = "sidebarBlock";

    const blockHeader = document.createElement("div");
    blockHeader.className = "head";
    blockHeader.innerText = text;

    const contentBlock = document.createElement("div");
    contentBlock.className = "bg";

    if(!enabled){
        toggleContentBlock(checkbox, contentBlock)
    }

    blockHeader.onclick = () => toggleContentBlock(checkbox, contentBlock);

    blockHeader.prepend(checkbox);
    block.appendChild(blockHeader);
    block.appendChild(contentBlock);
    domSidebar.appendChild(block);
    return contentBlock;
}

function toggleElementDisplay(element){
    element.style.display = element.style.display === "none" ? "block" : "none";
}

function toggleSidebar(checkbox, element){
    const enabled = element.style.display === "none";
    element.style.display = enabled ? "block" : "none";
    checkbox.checked = enabled;
}

function toggleContentBlock(checkbox, element){
    checkbox.checked = element.hidden;
    element.hidden = !element.hidden;
}
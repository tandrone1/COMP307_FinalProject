//global variables
var cartMap = new Map();
var totalItems = 0;
var totalPrice = 0;
var itemIDString = "";
var emptyCartUI;
var itemInventories = new Map(); //<id, quantity>

function insertCartMap(key, value){
    //helper function for inserting a value into a Map<key, Array>
    if(cartMap.has(key)){
        var items = cartMap.get(key);
        items.push(value);
        cartMap.set(key, items);
    }else{
        var items = new Array();
        items.push(value);
        cartMap.set(key, items);

    }
}

function storeCart(){
    //stores the cart data
    if(typeof(Storage)!=="undefined"){

        var cart = document.getElementById("cartDiv").innerHTML;
        window.localStorage.setItem('cart', cart);

        window.localStorage.setItem('cartMap', JSON.stringify(Array.from( cartMap.entries() ) ) );
       
        window.localStorage.setItem('totalItems',JSON.stringify(totalItems));
            

        window.localStorage.setItem('totalPrice', JSON.stringify(totalPrice));

        window.localStorage.setItem('itemIDString', itemIDString);

        window.localStorage.setItem('itemInventories', JSON.stringify(Array.from( itemInventories.entries() ) ))


    }
}

function loadCart(){
        
    //called onload: restores all the cart objects when the page is reloaded

    //load objects
    cartMap = new Map(JSON.parse(window.localStorage.getItem('cartMap')));
    
    totalItems = JSON.parse(window.localStorage.getItem('totalItems'));
        
    totalPrice =JSON.parse(window.localStorage.getItem('totalPrice'));

    itemIDString = window.localStorage.getItem('itemIDString');

    //load the UI
    var cart = document.getElementById("cartDiv");
    if(window.localStorage.getItem('cart')!=null){
            
        cart.innerHTML = window.localStorage.getItem('cart');
        updateCart();
    }
    /*disable add buttons if the number of items in the cart 
    is equal to the number in the inventory*/
    itemInventories = new Map(JSON.parse(window.localStorage.getItem('itemInventories')));

    for(var i=0; i< Array.from(itemInventories.keys()).length; i++){
        var key = Array.from(itemInventories.keys())[i];
        var inventory = itemInventories.get(key);
        if(cartMap.has(key)){  
            if(inventory == cartMap.get(key).length){

                disableAddButton(true, key);
            }
        }

    }
        
}
    
    

function addItem(id, title, price, img, inventory){
    //input inventory of item in dictionary
    itemInventories.set(id, inventory);
        
    //create a new item
    var item = { 
        id: id, 
        title: title,
        price: price,
        img: img
    };

    insertCartMap(id, item);
    var quantity = cartMap.get(id).length;

    totalItems++;
    
    //update the number of items in the cart
    updateCart();
    //update the price
    totalPrice += item.price;


    if(totalItems == 1){
    //first itme in the cart  
        setUpCartUI();
            
    }else{

        updatePrice()
    }

    //update UI
    if(quantity == 1){
        UIaddNewItem(item); 
            
    }else{
        updateQuantity(item.id);
           
    }

    if(cartMap.has(id)){

        if(itemInventories.get(id) == cartMap.get(id).length){
            disableAddButton(true, id);
        }

    }
    //update string of ids
    itemIDstoString();

    //store the updated cart
    storeCart()
    
}

function setUpCartUI(){
    //store the html for the empty cart
    emptyCartUI = document.getElementById("cartDiv").innerHTML;
    window.localStorage.setItem('emptyCart', emptyCartUI);
    //remove text that says "Empty Cart"
    var fillerText = document.getElementById("cartText");
    fillerText.parentNode.removeChild(fillerText);
    //remove image with empty cart icon
    var fillerImg = document.getElementById("cartFiller");
    fillerImg.parentNode.removeChild(fillerImg);
            
     var cartDiv = document.getElementById("cartPrice");
    //create total price row
    var pricePara = document.createElement("P");
    pricePara.setAttribute("id", "pricePara");
    var priceText= document.createTextNode("Total: $" + totalPrice.toFixed(2));
    pricePara.appendChild(priceText);
    cartDiv.appendChild(pricePara);

    //create checkout button
    createCheckoutButton();

}

function createCheckoutButton(){

    var form = document.getElementById("checkoutForm");

        

    var checkoutButton =document.createElement("BUTTON");
    checkoutButton.setAttribute("type", "submit");
    checkoutButton.setAttribute("value", "Checkout");
    checkoutButton.setAttribute("name", "Checkout");
    checkoutButton.setAttribute("class", "btn btn-primary");

    checkoutButton.setAttribute("id", "checkout"); 
    var checkoutText = document.createTextNode("View Cart");

        
    checkoutButton.appendChild(checkoutText);

        
    form.appendChild(checkoutButton);

    var input = document.createElement("INPUT");
    input.setAttribute("type", "hidden");
    input.setAttribute("id", "checkInput");
    input.setAttribute("name", "checkInput");
        

    input.setAttribute("value", itemIDString);

    form.appendChild(input);

}

function updatePrice(){
    //updates the price when an item is added or removed from cart
    var cartPrice = document.getElementById("cartPrice");
    var priceParaRm= document.getElementById("pricePara");
    priceParaRm.parentNode.removeChild(priceParaRm);

    pricePara = document.createElement("P");
    pricePara.setAttribute("id", "pricePara");
    priceText = document.createTextNode("Total: $" + totalPrice.toFixed(2));
    pricePara.appendChild(priceText);
    cartPrice.appendChild(pricePara);
            
    
}

function UIaddNewItem(item){
        
    //updating cart UI
    var cart = document.getElementById("cartTable");
    var row = document.createElement("TR");
    row.setAttribute("id", item.id);
    row.setAttribute("class", "cartRow");
        
    //image in cart
    var imgCell = document.createElement("TD");
    var img = document.createElement("IMG");
    img.setAttribute("src", "static/images/" +item.img);
    img.setAttribute("width", "80")
    imgCell.appendChild(img);
    row.appendChild(imgCell);

    //name and price item in cart

    var titleCell = document.createElement("TD");
    //title
    var titleBold = document.createElement("B");
    var title = document.createTextNode(item.title);
    titleBold.appendChild(title);

    var newLine= document.createElement("BR");
    //price
    var priceSmall = document.createElement("SMALL");
    var price = document.createTextNode("$" + item.price.toFixed(2));
    priceSmall.appendChild(price);

    titleCell.appendChild(titleBold);
    titleCell.appendChild(newLine);
    titleCell.appendChild(priceSmall);
    titleCell.setAttribute("class", "titleCell");
    row.appendChild(titleCell);

       
    //create remove button for item
    var removeButtonCell = document.createElement("TD");
    var removeButton = document.createElement("BUTTON");
    removeButton.setAttribute("class", "btn icon-btn");
    removeButton.setAttribute("type", "submit");
    removeButton.setAttribute("onclick", "removeItem(" + item.id + ")");
    var removeText = document.createTextNode("-");
    removeButton.appendChild(removeText);
    removeButtonCell.appendChild(removeButton);
    row.appendChild(removeButtonCell);
        
    //create quantity cell
    var quantity = cartMap.get(item.id).length;
    var quantityCell = document.createElement("TD");
    quantityCell.setAttribute("id", "qty" + item.id);
    var quantityText = document.createTextNode(quantity);
    quantityCell.appendChild(quantityText);
    row.appendChild(quantityCell);
    cart.appendChild(row);

    //create add button
    var addButtonCell = document.createElement("TD");
    var addButton = document.createElement("BUTTON");
    addButton.setAttribute("type", "submit");
    addButton.setAttribute("class", "btn icon-btn addbtn" + item.id);
    addButton.setAttribute("onclick", "addItem(" + item.id + ", \"" + item.title + "\"," + item.price + ",\"" + item.img + "\", " + itemInventories.get(item.id) + ")");
    var addText = document.createTextNode("+");
    addButton.appendChild(addText);
    addButtonCell.appendChild(addButton);
    row.appendChild(addButtonCell);


}

function updateQuantity(itemID){
    //update the quantity in cart
    var itemQty = document.getElementById("qty" + itemID);
    var quantity = cartMap.get(itemID).length;
    var quantityText = document.createTextNode(quantity);

    itemQty.replaceChild(quantityText, itemQty.childNodes[0]);


}

function removeItem(id){
        
    var price = cartMap.get(id).pop().price;
    var newQty = cartMap.get(id).length;
    totalPrice -= price;

    totalItems--;
    updateCart();
    if(newQty > 0){
        updateQuantity(id);

        //reenable add button
        if(cartMap.has(id)){  

            if(itemInventories.get(id) > cartMap.get(id).length){
                disableAddButton(false, id);
            }
        }
            
    }else{
        //remove the row if there are none left in the cart
        cartMap.delete(id);
        var cart = document.getElementById("cartTable");
            
        var removeRow = document.getElementById(id);
        removeRow.parentNode.removeChild(removeRow);

        //reenable add button
        disableAddButton(false, id);
            
    }
        
    

    if(totalItems== 0){
        loadEmptyCart();

    }else{
        updatePrice();
           
    }
    itemIDstoString();
    //store the cart when an item is removed
    storeCart();

}

function disableAddButton(disable, id){

    var addButtons = document.getElementsByClassName("addbtn" + id);
        for(var i =0; i< addButtons.length; i++){
            addButtons[i].disabled = disable;
        }
}
    
function loadEmptyCart(){

    var cart = document.getElementById("cartDiv");
    cart.innerHTML = window.localStorage.getItem('emptyCart');
        
}

function updateCart(){
    //updates number of items in cart
        
    //remove previous cart count
    var cartList = document.getElementById("cartList");
    var rmObj = document.getElementById("cart");

    var cart = document.createElement("a");
    cart.setAttribute("class", "nav-link dropdown-toggle");
    cart.setAttribute("href", "/");
    cart.setAttribute("role", "button");
    cart.setAttribute("data-toggle", "dropdown");
    cart.setAttribute("aria-haspopup", "true");
    cart.setAttribute("aria-expanded", "false");
    cart.setAttribute("id", "cart");

    var cartText = document.createTextNode("Cart(" + totalItems + ")");
    cart.appendChild(cartText);
    //replace with new cart count
    cartList.replaceChild(cart, rmObj);
        
}
    
function itemIDstoString(){
      //sends the correct value to the input to be later used when checking out  
    var IDstr = "";
        
        
    for(var i=0; i< Array.from(cartMap.keys()).length; i++){
        var key = Array.from(cartMap.keys())[i];
        for(var j=0; j< cartMap.get(key).length; j++){
            IDstr += cartMap.get(key)[j].id;
                
            if(i < Array.from(cartMap.keys()).length-1 || j < cartMap.get(key).length-1){
                IDstr +=",";
            }
        }
    }

    itemIDString = IDstr;
    //update ID string
    var input = document.getElementById("checkInput");
    input.setAttribute("value", itemIDString);
        
    

}

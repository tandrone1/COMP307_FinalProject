
    var cartItems = new Array();
    var cartMap = new Map();
    var autoIndex = 0;
    var totalPrice = 0;

    function insertCartMap(key, value){
        if(cartMap.has(key)){
            var items = cartMap.get(key);
            items.add(value);
            cartMap.set(key, items);
        }else{
            var items = new Array();
            items.push(value);
            cartMap.set(key, items);

        }
    }
    
    function addItem(id, title, description, price, author, img){
    // console.log("item " + title + " added");
        
        
        var item = {index:autoIndex, 
            id: id, 
            title: title,
            description: description,
            price: price,
            author: author,
            img: img};
        cartItems.push(item);
        updateCart();
        // var i = cartItems.length -1;
        // if(autoIndex !=5){
        //      updateCart();
        // }
       


        var cart = document.getElementById("cartTable");
        var row = document.createElement("TR");
        row.setAttribute("id", autoIndex);
        autoIndex++;
        //image in cart
        var imgCell = document.createElement("TD");
        var img = document.createElement("IMG");
        img.setAttribute("src", "static/images/" +item.img);
        img.setAttribute("width", "40")
        imgCell.appendChild(img);
        row.appendChild(imgCell);

        //name of item in cart
        var titleCell = document.createElement("TD");
        var title = document.createTextNode(title);
        titleCell.appendChild(title);
        row.appendChild(titleCell);

        //price in cart
        var priceCell = document.createElement("TD");
        var price = document.createTextNode("$" + price.toFixed(2));
        priceCell.appendChild(price);
        row.appendChild(priceCell);

        //add to total price
        totalPrice += item.price;

        //create remove button for item
        var removeButton = document.createElement("BUTTON");
        removeButton.setAttribute("type", "submit");
        var removeText = document.createTextNode("-");
        removeButton.appendChild(removeText);
        row.appendChild(removeButton);
        removeButton.setAttribute("onclick", "removeItem(" + item.index + ")");


        cart.appendChild(row);
        
        if(cartItems.length==1){
            //remove filler text
            var fillerText = document.getElementById("cartFiller");
            fillerText.parentNode.removeChild(fillerText);
            

            var cartDiv = document.getElementById("cartDiv");
            //create total price row
            var pricePara = document.createElement("P");
            pricePara.setAttribute("id", "pricePara");
            var priceText= document.createTextNode("Total: $" + totalPrice.toFixed(2));
            pricePara.appendChild(priceText);
            cartDiv.appendChild(pricePara);

            //create checkout button
            var checkoutButton =document.createElement("BUTTON");
            checkoutButton.setAttribute("type", "submit");
            checkoutButton.setAttribute("id", "checkout");
            var checkoutText = document.createTextNode("Checkout");
            checkoutButton.appendChild(checkoutText);
            cartDiv.appendChild(checkoutButton);
           
        }else{
            var cartDiv = document.getElementById("cartDiv");
            var priceParaRm= document.getElementById("pricePara");
            priceParaRm.parentNode.removeChild(priceParaRm);

            pricePara = document.createElement("P");
            pricePara.setAttribute("id", "pricePara");
            priceText = document.createTextNode("Total: $" + totalPrice.toFixed(2));
            pricePara.appendChild(priceText);
            cartDiv.appendChild(pricePara);

        }
    
    }

    function removeItem(index){
        
        

        for(var i=0; i < cartItems.length; i++){
           if(cartItems[i].index== index){
                var price = cartItems[i].price;
                totalPrice -= price;
                cartItems.splice(i, 1);
                break;
            }
        }

        updateCart();
        console.log(index);
        var cart = document.getElementById("cartTable");
        var removeRow = document.getElementById(index);
        cart.removeChild(removeRow);

        if(cartItems.length == 0){
            var checkoutButton = document.getElementById("checkout");
            checkoutButton.parentNode.removeChild(checkoutButton);

            var emptyCart = document.createElement("p");
            emptyCart.setAttribute("id", "cartFiller");
            var fillerText = document.createTextNode("Empty Cart");
            emptyCart.appendChild(fillerText);
            cart.appendChild(emptyCart);

            var priceParaRm= document.getElementById("pricePara");
            priceParaRm.parentNode.removeChild(priceParaRm);

        }else{
            //update price
            var cartDiv = document.getElementById("cartDiv");
            var priceParaRm= document.getElementById("pricePara");
            priceParaRm.parentNode.removeChild(priceParaRm);

            pricePara = document.createElement("P");
            pricePara.setAttribute("id", "pricePara");
            priceText = document.createTextNode("Total: $" + totalPrice.toFixed(2));
            pricePara.appendChild(priceText);
            cartDiv.appendChild(pricePara);
        }

        

    }

    function updateCart(){

        // //remove filler text
        // var fillerText = document.getElementById("cartFiller");
        // fillerText.parentNode.removeChild(fillerText);
        

        var cartList = document.getElementById("cartList");
        var rmObj = document.getElementById("cart");

        

        var cart = document.createElement("a");
        cart.setAttribute("class", "nav-link dropdown-toggle");
        cart.setAttribute("href", "/");
        // cart.setAttribute("id", "navbarDropdownMenuLink");
        cart.setAttribute("role", "button");
        cart.setAttribute("data-toggle", "dropdown");
        cart.setAttribute("aria-haspopup", "true");
        cart.setAttribute("aria-expanded", "false");
        cart.setAttribute("id", "cart");
        var cartText = document.createTextNode("Cart(" + cartItems.length + ")");
        cart.appendChild(cartText);

        cartList.replaceChild(cart, rmObj);
        // var cartList = document.getElementById("cartList");
        // cartList.appendChild(cart);

    }

    
    function checkout(){
        console.log("checkout");
    
    }

    
  
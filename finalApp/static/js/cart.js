var cartItems = new Array();
    var cartMap = new Map();
    var autoIndex = 0;
    var totalPrice = 0;
    var itemIDString = "";

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
    
    function createCheckoutButton(){
        // var form = document.createElement("FORM");
        // form.setAttribute("method", 'post');
        // form.setAttribute("action", '#');

        // var csrf_token = document.createTextNode(" {% csrf_token %} ");
        // form.appendChild(csrf_token);
        var form = document.getElementById("checkoutForm");

        var checkoutButton =document.createElement("BUTTON");
        checkoutButton.setAttribute("type", "submit");
        checkoutButton.setAttribute("value", "Checkout");
        checkoutButton.setAttribute("name", "Checkout");
        // checkoutButton.setAttribute("onclick", "checkout()");
        checkoutButton.setAttribute("id", "checkout"); 
        var checkoutText = document.createTextNode("Checkout");
        checkoutButton.appendChild(checkoutText);

        form.appendChild(checkoutButton);

        var input = document.createElement("INPUT");
        input.setAttribute("type", "hidden");
        input.setAttribute("id", "checkInput");
        input.setAttribute("name", "checkInput");
        itemIDstoString();
        input.setAttribute("value", itemIDString);

        form.appendChild(input);

        // var cartDiv = document.getElementById("cartDiv");
        // cartDiv.appendChild(form);
    }

    function addItem(id, title, description, price, author, img){
    // console.log("item " + title + " added");
        
        //create a new item
        var item = {index:autoIndex, 
            id: id, 
            title: title,
            description: description,
            price: price,
            author: author,
            img: img};

        //add the item to the cartItem array    
        cartItems.push(item);

        //update the number of items in the cart
        updateCart();
      

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

        //update string of ids
        itemIDstoString();

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

          
            createCheckoutButton();
           
        }else{
            //update total price
            var cartDiv = document.getElementById("cartDiv");
            var priceParaRm= document.getElementById("pricePara");
            priceParaRm.parentNode.removeChild(priceParaRm);

            pricePara = document.createElement("P");
            pricePara.setAttribute("id", "pricePara");
            priceText = document.createTextNode("Total: $" + totalPrice.toFixed(2));
            pricePara.appendChild(priceText);
            cartDiv.appendChild(pricePara);

            //update ID string
            var input = document.getElementById("checkInput");
            input.setAttribute("value", itemIDString);

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
        //update string of ids
        itemIDstoString();

        // console.log(index);
        var cart = document.getElementById("cartTable");
        var removeRow = document.getElementById(index);
        cart.removeChild(removeRow);

        if(cartItems.length == 0){
            //remove checkout button @TODO this needs to change to remove the whole form
            var checkoutButton = document.getElementById("checkout");
            checkoutButton.parentNode.removeChild(checkoutButton);
            //remove checkout input
            var checkoutInput = document.getElementById("checkInput");
            checkoutInput.parentNode.removeChild(checkoutInput);

            //add filler text
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

            //update ID string
            var input = document.getElementById("checkInput");
            itemIDstoString();
            input.setAttribute("value", itemIDString);
        }

        

    }

    function updateCart(){
        //updates number of items in cart
        
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
        

    }

    
    function checkout(){
        // itemIDstoString();

        // // console.log("checkout");
        // // var itemIDs = new Array();
        // // for(var i =0; i< cartItems.length;i++){
        // //     itemIDs.push(cartItems[i].id);
            
        // // }
        // // var itemstr = itemIDstoString(itemIDs);

        // var input = document.getElementById("checkInput");
        // input.setAttribute("value", itemIDString);
        // console.log(itemIDString);

        // var form = document.createElement("FORM");
        // form.setAttribute("method", 'post');
        // form.setAttribute("action", '#');

        // var csrf_token = document.createTextNode(" {% csrf_token %} ");
        // form.appendChild(csrf_token);

        // var checkoutButton = document.getElementById("checkout");
        // form.appendChild(checkoutButton);

        // var input = document.createElement("INPUT");
        // input.setAttribute("type", "hidden");
        // input.setAttribute("id", "check");
        // input.setAttribute("name", "check");
        // input.setAttribute("value", itemstr);

        // form.appendChild(input);
//         <form method='post' action='#'>
//   {% csrf_token %} 
//   <button type="submit" value="Checkout" name='Checkout' onclick="checkout()">Checkout</button>
//   <input type="hidden" id="pl" name="pl" value="checkout">

// </form>
        // return itemIDs;
    }

    function itemIDstoString(){


        var IDstr = "{";
        for(var i=0; i<cartItems.length;i++){
            IDstr += cartItems[i].id;
            if(i<cartItems.length-1){
                IDstr+=",";
            }
        }
        IDstr +="}";
        // console.log(IDstr);
        itemIDString = IDstr;

    }
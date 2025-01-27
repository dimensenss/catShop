document.addEventListener("DOMContentLoaded", function () {
    var loaderWrapper = document.getElementById("loader-wrapper");
    if (loaderWrapper) {
        loaderWrapper.style.display = "none";
    }
});

$(document).ready(function ($) {
    var successMessage = $("#jq-notification");
    var notification = $('#notification');
    var warning_notification = $('#warning-jq-notification');

    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');

        }, 3000);
    }


    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();
        var goodsInCartCount = $(".goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.first().text() || 0);

        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");
        var is_order = $(this).data("is-order");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                is_order: is_order,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 1500);
                cartCount++;
                console.log(data.success_add);
                if(data.success_add === "0"){
                    cartCount -= 1;
                }
                goodsInCartCount.text(cartCount);

                var cartItemsContainer = $(".cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                if (is_order) {
                    var createOrderUrl = data.create_order_url;
                    window.location.href = createOrderUrl;
                }
            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });


    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $(".goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.first().text() || 0); // Выбираем первый элемент

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 1500);

                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);


                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $(".cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    var isUpdatingCart = false; // Флаг, который указывает, идет ли в данный момент процесс обновления корзины

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Сообщение

                // Изменяем количество товаров в корзине
                var goodsInCartCount = $(".goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.first().text() || 0); // Выбираем первый элемент
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $(".cart-items-container");
                cartItemsContainer.html(data.cart_items_html);


            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }

    $(document).on("input", ".number", function () {
        if (!isUpdatingCart) {
            isUpdatingCart = true;

            var url = $(this).closest('.input-group').find('.increment').data("cart-change-url");
            var cartID = $(this).closest('.input-group').find('.increment').data("cart-id");
            var quantity = parseInt($(this).val());

            // Проверяем, что количество находится в допустимом диапазоне
            if (quantity >= 1 && quantity <= 9999) {
                updateCart(cartID, quantity, quantity - parseInt($(this).attr('value')), url);

                // Устанавливаем задержку (при необходимости)
                setTimeout(function () {
                    isUpdatingCart = false;
                }, 200);
            } else {
                // Возвращаем предыдущее значение в случае недопустимого количества
                $(this).val(parseInt($(this).attr('value')));
                isUpdatingCart = false;
            }
        }
    });

    $(document).on("click", ".decrement", function () {
        if (!isUpdatingCart) {
            isUpdatingCart = true;

            var url = $(this).data("cart-change-url");
            var cartID = $(this).data("cart-id");
            var $input = $(this).closest('.input-group').find('.number');
            var currentValue = parseInt($input.val());

            if (currentValue > 1) {
                $input.val(currentValue - 1);
                updateCart(cartID, currentValue - 1, -1, url);
            }

            setTimeout(function () {
                isUpdatingCart = false;
            }, 200);
        }
    });

    $(document).on("click", ".increment", function () {
        if (!isUpdatingCart) {
            isUpdatingCart = true;

            var url = $(this).data("cart-change-url");
            var cartID = $(this).data("cart-id");
            var $input = $(this).closest('.input-group').find('.number');
            var currentValue = parseInt($input.val());

            $input.val(currentValue + 1);
            updateCart(cartID, currentValue + 1, 1, url);

            setTimeout(function () {
                isUpdatingCart = false;
            }, 200);
        }
    });


    $(document).on("click", ".btn-delete-review", function (e) {
        e.preventDefault();

        var review_id = $(this).data("review_id");
        var product_id = $(this).data("product_id");
        var view_url = $(this).data('view_url')

        $.ajax({

            type: "GET",
            url: view_url,
            data: {
                review_id: review_id,
                product_id: product_id,
            },
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 1500);


                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var review_container = $(".review-container");
                review_container.html(data.review_container);

            },

            error: function (data) {
                console.log("Помилка при видаленні відгука");
            },
        });
    });
    $(document).on("click", ".add-to-wish-list", function (e) {
  e.preventDefault();

  var goodsInWishListCount = $(".product_in_wish_list_count");
  var wishCount = parseInt(goodsInWishListCount.first().text() || 0);

  var $this = $(this);
  var product_id = $this.data("product-id");
  var add_to_wish_list_url = $this.attr("href");

  $.ajax({
    type: "POST",
    url: add_to_wish_list_url,
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {
      successMessage.html(data.message);
      successMessage.fadeIn(400);
      setTimeout(function () {
        successMessage.fadeOut(400);
      }, 1500);

      wishCount = data.change_value + wishCount;
      goodsInWishListCount.text(wishCount);

      var WishListContainer = $(".wish-list-container");
      if (WishListContainer.length > 0) {
        WishListContainer.html(data.wish_list_container);
      }

      // Обновляем класс иконки сердца и текст, если параграф существует
      var wishIcon = $this.find('.wish-icon');
      var parentParagraph = $this.closest('p.product-base-info');
      if (parentParagraph.length > 0) {
        if (wishIcon.hasClass('fa-regular')) {
          wishIcon.removeClass('fa-regular fa-heart').addClass('fa-solid fa-heart');
          parentParagraph.contents().filter(function() {
            return this.nodeType === 3; // Узел текста
          }).first().replaceWith('Видалити з бажаного ');
        } else {
          wishIcon.removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');
          parentParagraph.contents().filter(function() {
            return this.nodeType === 3; // Узел текста
          }).first().replaceWith('Додати в бажання &nbsp; ');
        }
      } else {
        // Только переключаем иконку сердца, если параграфа нет
        if (wishIcon.hasClass('fa-regular')) {
          wishIcon.removeClass('fa-regular fa-heart').addClass('fa-solid fa-heart');
        } else {
          wishIcon.removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');
        }
      }
    },

    error: function (data) {
      console.log("Ошибка при добавлении в список желаний");
    },
  });
});



});
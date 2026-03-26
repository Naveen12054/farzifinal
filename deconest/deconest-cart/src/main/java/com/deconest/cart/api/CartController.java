package com.deconest.cart.api;

import com.deconest.cart.api.dto.AddCartItemRequest;
import com.deconest.cart.api.dto.AddWishlistItemRequest;
import com.deconest.cart.api.dto.CartSummaryResponse;
import com.deconest.cart.api.dto.UpdateCartItemQuantityRequest;
import com.deconest.cart.api.dto.WishlistItemResponse;
import com.deconest.cart.service.CartService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/cart")
public class CartController {

    private final CartService cartService;

    public CartController(CartService cartService) {
        this.cartService = cartService;
    }

    @GetMapping("/items")
    public CartSummaryResponse getCurrentCart(Authentication authentication) {
        return cartService.getCurrentCart(authentication.getName());
    }

    @PostMapping("/items")
    public CartSummaryResponse addCartItem(
            Authentication authentication,
            @Valid @RequestBody AddCartItemRequest request) {
        return cartService.addCartItem(authentication.getName(), request);
    }

    @PutMapping("/items/{itemId}")
    public CartSummaryResponse updateCartItem(
            Authentication authentication,
            @PathVariable Long itemId,
            @Valid @RequestBody UpdateCartItemQuantityRequest request) {
        return cartService.updateCartItem(authentication.getName(), itemId, request);
    }

    @DeleteMapping("/items/{itemId}")
    public CartSummaryResponse removeCartItem(Authentication authentication, @PathVariable Long itemId) {
        return cartService.removeCartItem(authentication.getName(), itemId);
    }

    @GetMapping("/wishlist")
    public List<WishlistItemResponse> getCurrentWishlist(Authentication authentication) {
        return cartService.getCurrentWishlist(authentication.getName());
    }

    @PostMapping("/wishlist")
    public List<WishlistItemResponse> addWishlistItem(
            Authentication authentication,
            @Valid @RequestBody AddWishlistItemRequest request) {
        return cartService.addWishlistItem(authentication.getName(), request);
    }

    @DeleteMapping("/wishlist/{productId}")
    public List<WishlistItemResponse> removeWishlistItem(
            Authentication authentication,
            @PathVariable Long productId) {
        return cartService.removeWishlistItem(authentication.getName(), productId);
    }
}

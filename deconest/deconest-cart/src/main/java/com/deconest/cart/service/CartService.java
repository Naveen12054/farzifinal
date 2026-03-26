package com.deconest.cart.service;

import com.deconest.cart.api.dto.AddCartItemRequest;
import com.deconest.cart.api.dto.AddWishlistItemRequest;
import com.deconest.cart.api.dto.CartItemResponse;
import com.deconest.cart.api.dto.CartSummaryResponse;
import com.deconest.cart.api.dto.UpdateCartItemQuantityRequest;
import com.deconest.cart.api.dto.WishlistItemResponse;
import com.deconest.cart.domain.CartItem;
import com.deconest.cart.domain.WishlistItem;
import com.deconest.cart.repository.CartItemRepository;
import com.deconest.cart.repository.WishlistItemRepository;
import com.deconest.catalog.domain.Product;
import com.deconest.catalog.domain.ProductStatus;
import com.deconest.catalog.repository.ProductRepository;
import com.deconest.user.domain.UserAccount;
import com.deconest.user.repository.UserAccountRepository;
import jakarta.persistence.EntityExistsException;
import jakarta.persistence.EntityNotFoundException;
import java.math.BigDecimal;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class CartService {

    private final CartItemRepository cartItemRepository;
    private final WishlistItemRepository wishlistItemRepository;
    private final UserAccountRepository userAccountRepository;
    private final ProductRepository productRepository;

    public CartService(
            CartItemRepository cartItemRepository,
            WishlistItemRepository wishlistItemRepository,
            UserAccountRepository userAccountRepository,
            ProductRepository productRepository) {
        this.cartItemRepository = cartItemRepository;
        this.wishlistItemRepository = wishlistItemRepository;
        this.userAccountRepository = userAccountRepository;
        this.productRepository = productRepository;
    }

    @Transactional(readOnly = true)
    public CartSummaryResponse getCurrentCart(String email) {
        List<CartItemResponse> items = cartItemRepository.findByUserEmailOrderByCreatedAtAsc(email).stream()
                .map(this::toResponse)
                .toList();

        BigDecimal subtotal = items.stream()
                .map(CartItemResponse::lineTotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        int totalItems = items.stream()
                .map(CartItemResponse::quantity)
                .reduce(0, Integer::sum);

        return new CartSummaryResponse(totalItems, subtotal, items);
    }

    public CartSummaryResponse addCartItem(String email, AddCartItemRequest request) {
        UserAccount user = getUser(email);
        Product product = getPurchasableProduct(request.productId());
        validateRequestedQuantity(request.quantity(), product);

        CartItem cartItem = cartItemRepository.findByUserEmailAndProductId(email, request.productId())
                .orElse(null);

        if (cartItem == null) {
            cartItemRepository.save(new CartItem(user, product, request.quantity()));
        } else {
            int updatedQuantity = cartItem.getQuantity() + request.quantity();
            validateRequestedQuantity(updatedQuantity, product);
            cartItem.updateQuantity(updatedQuantity);
        }

        return getCurrentCart(email);
    }

    public CartSummaryResponse updateCartItem(String email, Long itemId, UpdateCartItemQuantityRequest request) {
        CartItem cartItem = cartItemRepository.findByIdAndUserEmail(itemId, email)
                .orElseThrow(() -> new EntityNotFoundException("Cart item not found: " + itemId));
        validateRequestedQuantity(request.quantity(), cartItem.getProduct());
        cartItem.updateQuantity(request.quantity());
        return getCurrentCart(email);
    }

    public CartSummaryResponse removeCartItem(String email, Long itemId) {
        CartItem cartItem = cartItemRepository.findByIdAndUserEmail(itemId, email)
                .orElseThrow(() -> new EntityNotFoundException("Cart item not found: " + itemId));
        cartItemRepository.delete(cartItem);
        return getCurrentCart(email);
    }

    @Transactional(readOnly = true)
    public List<WishlistItemResponse> getCurrentWishlist(String email) {
        return wishlistItemRepository.findByUserEmailOrderByCreatedAtAsc(email).stream()
                .map(this::toResponse)
                .toList();
    }

    public List<WishlistItemResponse> addWishlistItem(String email, AddWishlistItemRequest request) {
        UserAccount user = getUser(email);
        Product product = getPurchasableProduct(request.productId());

        if (wishlistItemRepository.findByUserEmailAndProductId(email, request.productId()).isPresent()) {
            throw new EntityExistsException("Product already exists in wishlist: " + request.productId());
        }

        wishlistItemRepository.save(new WishlistItem(user, product));
        return getCurrentWishlist(email);
    }

    public List<WishlistItemResponse> removeWishlistItem(String email, Long productId) {
        WishlistItem item = wishlistItemRepository.findByUserEmailAndProductId(email, productId)
                .orElseThrow(() -> new EntityNotFoundException("Wishlist item not found for product: " + productId));
        wishlistItemRepository.delete(item);
        return getCurrentWishlist(email);
    }

    private UserAccount getUser(String email) {
        return userAccountRepository.findByEmail(email)
                .orElseThrow(() -> new EntityNotFoundException("User not found with email: " + email));
    }

    private Product getPurchasableProduct(Long productId) {
        Product product = productRepository.findById(productId)
                .orElseThrow(() -> new EntityNotFoundException("Product not found: " + productId));

        if (product.getStatus() != ProductStatus.ACTIVE) {
            throw new IllegalStateException("Product is not available for purchase: " + productId);
        }

        return product;
    }

    private void validateRequestedQuantity(Integer requestedQuantity, Product product) {
        if (requestedQuantity > product.getQuantity()) {
            throw new IllegalArgumentException(
                    "Requested quantity exceeds available stock for product: " + product.getId());
        }
    }

    private CartItemResponse toResponse(CartItem cartItem) {
        Product product = cartItem.getProduct();
        BigDecimal unitPrice = product.getPrice();
        BigDecimal lineTotal = unitPrice.multiply(BigDecimal.valueOf(cartItem.getQuantity()));
        return new CartItemResponse(
                cartItem.getId(),
                product.getId(),
                product.getName(),
                product.getSeller().getFullName(),
                unitPrice,
                cartItem.getQuantity(),
                lineTotal,
                product.getImageUrl1());
    }

    private WishlistItemResponse toResponse(WishlistItem wishlistItem) {
        Product product = wishlistItem.getProduct();
        return new WishlistItemResponse(
                wishlistItem.getId(),
                product.getId(),
                product.getName(),
                product.getSeller().getFullName(),
                product.getPrice(),
                product.getImageUrl1());
    }
}

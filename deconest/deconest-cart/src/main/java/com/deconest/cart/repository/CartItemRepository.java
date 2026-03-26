package com.deconest.cart.repository;

import com.deconest.cart.domain.CartItem;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CartItemRepository extends JpaRepository<CartItem, Long> {

    List<CartItem> findByUserEmailOrderByCreatedAtAsc(String email);

    Optional<CartItem> findByIdAndUserEmail(Long id, String email);

    Optional<CartItem> findByUserEmailAndProductId(String email, Long productId);
}

package com.deconest.cart.repository;

import com.deconest.cart.domain.WishlistItem;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface WishlistItemRepository extends JpaRepository<WishlistItem, Long> {

    List<WishlistItem> findByUserEmailOrderByCreatedAtAsc(String email);

    Optional<WishlistItem> findByUserEmailAndProductId(String email, Long productId);
}

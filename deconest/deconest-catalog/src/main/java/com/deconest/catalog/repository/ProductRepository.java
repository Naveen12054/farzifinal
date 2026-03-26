package com.deconest.catalog.repository;

import com.deconest.catalog.domain.Product;
import com.deconest.catalog.domain.ProductStatus;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Long> {

    List<Product> findByStatus(ProductStatus status);

    List<Product> findBySellerId(Long sellerId);

    List<Product> findByCategoryId(Long categoryId);
}


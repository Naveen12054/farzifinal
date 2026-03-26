package com.deconest.catalog.api.dto;

import com.deconest.catalog.domain.ProductStatus;
import java.math.BigDecimal;

public record ProductResponse(
        Long id,
        Long sellerId,
        Long categoryId,
        Long subcategoryId,
        String brandName,
        String name,
        String productDescription,
        String materialDescription,
        BigDecimal price,
        Integer quantity,
        String imageUrl1,
        String imageUrl2,
        String imageUrl3,
        String imageUrl4,
        String measurements,
        String maintenanceNotes,
        String color,
        ProductStatus status
) {
}


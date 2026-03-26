package com.deconest.catalog.api.dto;

import com.deconest.catalog.domain.ProductStatus;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;

public record CreateProductRequest(
        @NotNull Long sellerId,
        @NotNull Long categoryId,
        @NotNull Long subcategoryId,
        @Size(max = 120) String brandName,
        @NotBlank @Size(max = 180) String name,
        @Size(max = 4000) String productDescription,
        @Size(max = 2000) String materialDescription,
        @NotNull @DecimalMin("0.00") BigDecimal price,
        @NotNull @PositiveOrZero Integer quantity,
        @Size(max = 255) String imageUrl1,
        @Size(max = 255) String imageUrl2,
        @Size(max = 255) String imageUrl3,
        @Size(max = 255) String imageUrl4,
        @Size(max = 255) String measurements,
        @Size(max = 1000) String maintenanceNotes,
        @Size(max = 120) String color,
        ProductStatus status
) {
}


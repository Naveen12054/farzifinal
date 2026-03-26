package com.deconest.catalog.api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CreateCategoryRequest(
        @NotBlank @Size(max = 80) String name,
        @Size(max = 500) String description,
        @Size(max = 255) String imageUrl,
        boolean availableForSale,
        boolean availableForRent
) {
}


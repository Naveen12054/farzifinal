package com.deconest.catalog.api.dto;

public record CategoryResponse(
        Long id,
        String name,
        String description,
        String imageUrl,
        boolean enabled,
        boolean availableForSale,
        boolean availableForRent
) {
}


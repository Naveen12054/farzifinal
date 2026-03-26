package com.deconest.catalog.api.dto;

public record SubcategoryResponse(
        Long id,
        Long categoryId,
        String name,
        String description,
        boolean enabled
) {
}


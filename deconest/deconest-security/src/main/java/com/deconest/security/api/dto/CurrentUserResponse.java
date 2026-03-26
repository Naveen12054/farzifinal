package com.deconest.security.api.dto;

import com.deconest.user.domain.UserRole;

public record CurrentUserResponse(
        Long id,
        String email,
        String fullName,
        UserRole role,
        boolean active,
        boolean verified,
        boolean blacklisted
) {
}


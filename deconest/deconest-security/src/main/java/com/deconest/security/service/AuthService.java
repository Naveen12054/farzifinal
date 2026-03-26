package com.deconest.security.service;

import com.deconest.security.api.dto.AuthUserResponse;
import com.deconest.security.api.dto.CurrentUserResponse;
import com.deconest.security.api.dto.SignupRequest;
import com.deconest.user.api.dto.CreateUserRequest;
import com.deconest.user.api.dto.UserAccountResponse;
import com.deconest.user.service.UserService;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserService userService;

    public AuthService(UserService userService) {
        this.userService = userService;
    }

    public AuthUserResponse signup(SignupRequest request) {
        UserAccountResponse created = userService.createUser(new CreateUserRequest(
                request.email(),
                request.fullName(),
                request.password(),
                request.role()));

        return new AuthUserResponse(
                created.id(),
                created.email(),
                created.fullName(),
                created.role(),
                created.active(),
                created.verified());
    }

    public CurrentUserResponse currentUser(String email) {
        UserAccountResponse user = userService.getUserByEmail(email);

        return new CurrentUserResponse(
                user.id(),
                user.email(),
                user.fullName(),
                user.role(),
                user.active(),
                user.verified(),
                user.blacklisted());
    }
}

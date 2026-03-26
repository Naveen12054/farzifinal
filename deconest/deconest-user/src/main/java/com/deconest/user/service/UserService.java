package com.deconest.user.service;

import com.deconest.common.security.PasswordHasher;
import com.deconest.user.api.dto.CreateUserRequest;
import com.deconest.user.api.dto.UserAccountResponse;
import com.deconest.user.domain.DeliveryAgentProfile;
import com.deconest.user.domain.SellerProfile;
import com.deconest.user.domain.UserAccount;
import com.deconest.user.domain.UserProfile;
import com.deconest.user.domain.UserRole;
import com.deconest.user.repository.DeliveryAgentProfileRepository;
import com.deconest.user.repository.SellerProfileRepository;
import com.deconest.user.repository.UserAccountRepository;
import com.deconest.user.repository.UserProfileRepository;
import jakarta.persistence.EntityExistsException;
import jakarta.persistence.EntityNotFoundException;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class UserService {

    private final UserAccountRepository userAccountRepository;
    private final UserProfileRepository userProfileRepository;
    private final SellerProfileRepository sellerProfileRepository;
    private final DeliveryAgentProfileRepository deliveryAgentProfileRepository;
    private final PasswordHasher passwordHasher;

    public UserService(
            UserAccountRepository userAccountRepository,
            UserProfileRepository userProfileRepository,
            SellerProfileRepository sellerProfileRepository,
            DeliveryAgentProfileRepository deliveryAgentProfileRepository,
            PasswordHasher passwordHasher) {
        this.userAccountRepository = userAccountRepository;
        this.userProfileRepository = userProfileRepository;
        this.sellerProfileRepository = sellerProfileRepository;
        this.deliveryAgentProfileRepository = deliveryAgentProfileRepository;
        this.passwordHasher = passwordHasher;
    }

    public UserAccountResponse createUser(CreateUserRequest request) {
        if (userAccountRepository.existsByEmail(request.email())) {
            throw new EntityExistsException("User already exists with email: " + request.email());
        }

        UserAccount userAccount = new UserAccount(
                request.email(),
                request.fullName(),
                passwordHasher.hash(request.password()),
                request.role());

        UserAccount saved = userAccountRepository.save(userAccount);
        provisionDefaultProfile(saved);
        return toResponse(saved);
    }

    @Transactional(readOnly = true)
    public List<UserAccountResponse> listUsers() {
        return userAccountRepository.findAll().stream()
                .map(this::toResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public UserAccountResponse getUser(Long id) {
        UserAccount account = userAccountRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("User not found: " + id));
        return toResponse(account);
    }

    private void provisionDefaultProfile(UserAccount userAccount) {
        if (userAccount.getRole() == UserRole.SELLER) {
            sellerProfileRepository.save(new SellerProfile(userAccount));
            return;
        }

        if (userAccount.getRole() == UserRole.DELIVERY_AGENT) {
            deliveryAgentProfileRepository.save(new DeliveryAgentProfile(userAccount));
            return;
        }

        userProfileRepository.save(new UserProfile(userAccount));
    }

    private UserAccountResponse toResponse(UserAccount userAccount) {
        return new UserAccountResponse(
                userAccount.getId(),
                userAccount.getEmail(),
                userAccount.getFullName(),
                userAccount.getRole(),
                userAccount.isActive(),
                userAccount.isVerified(),
                userAccount.isBlacklisted());
    }
}

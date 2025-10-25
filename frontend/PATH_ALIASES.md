# Path Aliases Configuration

## Overview

This project uses **TypeScript path aliases** to simplify imports and avoid complex relative paths. This is a best practice that makes the codebase more maintainable and easier to refactor.

---

## Configured Aliases

| Alias | Resolves To | Usage |
|-------|-------------|-------|
| `@/*` | `src/*` | Import anything from `src/` |
| `@services/*` | `src/services/*` | Import from `src/services/` |
| `@pages/*` | `src/pages/*` | Import from `src/pages/` |
| `@components/*` | `src/components/*` | Import from `src/components/` |

---

## Benefits

### ❌ Before (Relative Paths)
```typescript
// Deep nesting becomes messy
import { authApi } from "../../../services/api";
import config from "../../../../config";

// Moving files breaks imports
// Hard to read and maintain
```

### ✅ After (Path Aliases)
```typescript
// Clean and consistent
import { authApi } from "@services/api";
import config from "@/config";

// Moving files is easier
// Clear and professional
```

---

## Configuration Files

### 1. TypeScript Configuration (`tsconfig.app.json`)

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@services/*": ["src/services/*"],
      "@pages/*": ["src/pages/*"],
      "@components/*": ["src/components/*"]
    }
  }
}
```

This tells TypeScript where to find the aliases during type checking.

### 2. Vite Configuration (`vite.config.ts`)

```typescript
import path from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@services': path.resolve(__dirname, './src/services'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@components': path.resolve(__dirname, './src/components'),
    },
  },
})
```

This tells Vite how to resolve the aliases during build/dev server.

### 3. Production Vite Configuration (`vite.prod.config.ts`)

Same alias configuration as `vite.config.ts` to ensure production builds work correctly.

---

## Usage Examples

### Importing API Service
```typescript
// ✅ Good - Using alias
import { peopleApi, typesApi } from "@services/api";
import type { Person, LeaveType } from "@services/api";

// ❌ Avoid - Relative path
import { peopleApi, typesApi } from "../services/api";
```

### Importing Config
```typescript
// ✅ Good - Using alias
import config from "@/config";

// ❌ Avoid - Relative path
import config from "../config";
```

### Importing Components (when created)
```typescript
// ✅ Good - Using alias
import { Button } from "@components/Button";
import { Header } from "@components/Header";

// ❌ Avoid - Relative path
import { Button } from "../../components/Button";
```

### Importing Pages (for routing)
```typescript
// ✅ Good - Using alias
import Dashboard from "@pages/Dashboard";
import Settings from "@pages/Settings";

// ❌ Avoid - Relative path
import Dashboard from "../pages/Dashboard";
```

---

## File Structure

```
frontend/
├── src/
│   ├── config.ts              → Import as: @/config
│   ├── main.tsx               → Import as: @/main
│   ├── services/
│   │   └── api.ts             → Import as: @services/api
│   ├── pages/
│   │   ├── Login.tsx          → Import as: @pages/Login
│   │   ├── Register.tsx       → Import as: @pages/Register
│   │   ├── Dashboard.tsx      → Import as: @pages/Dashboard
│   │   └── Settings.tsx       → Import as: @pages/Settings
│   └── components/            → Import as: @components/...
│       └── (future components)
├── tsconfig.app.json          → TypeScript path config
├── vite.config.ts             → Vite dev path config
└── vite.prod.config.ts        → Vite prod path config
```

---

## Current Imports (All Updated)

### ✅ Login.tsx
```typescript
import { authApi } from "@services/api";
```

### ✅ Register.tsx
```typescript
import { authApi } from "@services/api";
```

### ✅ Dashboard.tsx
```typescript
import { peopleApi, typesApi, absencesApi } from "@services/api";
import type { Person, LeaveType } from "@services/api";
```

### ✅ Settings.tsx
```typescript
import { peopleApi, typesApi } from "@services/api";
import type { Person, LeaveType } from "@services/api";
```

### ✅ api.ts
```typescript
import config from "@/config";
```

---

## Adding New Aliases (Future)

If you want to add more aliases (e.g., for `utils/`, `hooks/`, `types/`):

### 1. Update `tsconfig.app.json`
```jsonc
{
  "compilerOptions": {
    "paths": {
      "@/*": ["src/*"],
      "@services/*": ["src/services/*"],
      "@pages/*": ["src/pages/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"],        // 👈 Add this
      "@hooks/*": ["src/hooks/*"],        // 👈 Add this
      "@types/*": ["src/types/*"]         // 👈 Add this
    }
  }
}
```

### 2. Update `vite.config.ts` and `vite.prod.config.ts`
```typescript
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@services': path.resolve(__dirname, './src/services'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@components': path.resolve(__dirname, './src/components'),
      '@utils': path.resolve(__dirname, './src/utils'),        // 👈 Add this
      '@hooks': path.resolve(__dirname, './src/hooks'),        // 👈 Add this
      '@types': path.resolve(__dirname, './src/types'),        // 👈 Add this
    },
  },
})
```

### 3. Use the new aliases
```typescript
import { formatDate } from "@utils/formatters";
import { useAuth } from "@hooks/useAuth";
import type { User } from "@types/models";
```

---

## IDE Support

### VS Code
- ✅ IntelliSense fully supports path aliases
- ✅ Auto-import uses aliases automatically
- ✅ Go to Definition works with aliases
- ✅ Refactoring preserves aliases

### Other IDEs
Most modern TypeScript-aware IDEs (WebStorm, Sublime, etc.) support TypeScript path mapping via `tsconfig.json`.

---

## Troubleshooting

### Issue: "Cannot find module '@services/api'"

**Solution:**
1. Restart VS Code TypeScript server:
   - Open Command Palette (Ctrl+Shift+P)
   - Type: "TypeScript: Restart TS Server"
2. If still not working, check:
   - `tsconfig.app.json` has correct `paths` config
   - `vite.config.ts` has correct `alias` config
   - Run `npm run dev` to restart dev server

### Issue: Build fails with path alias errors

**Solution:**
Ensure `vite.prod.config.ts` has the same alias configuration as `vite.config.ts`.

### Issue: Tests don't resolve aliases

**Solution:**
If you add tests later (Jest/Vitest), configure module name mapping:

```javascript
// vitest.config.ts
export default defineConfig({
  test: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@services': path.resolve(__dirname, './src/services'),
      // ... other aliases
    },
  },
})
```

---

## Best Practices

### ✅ DO
- Use `@services/api` for service imports
- Use `@/config` for root-level files
- Use `@pages/*` for page imports
- Use `@components/*` for component imports
- Keep alias names short and intuitive

### ❌ DON'T
- Mix relative paths and aliases in the same file
- Create too many aliases (keep it simple)
- Use aliases for local imports (same directory)
- Change alias names frequently (breaking changes)

### Example: When to use relative vs. alias

```typescript
// ✅ Use alias for imports from different directories
import { authApi } from "@services/api";

// ✅ Use relative for imports in same directory
import { UserCard } from "./UserCard";
import type { UserProps } from "./types";
```

---

## Migration Checklist

✅ Configured TypeScript path aliases in `tsconfig.app.json`  
✅ Configured Vite aliases in `vite.config.ts`  
✅ Configured Vite aliases in `vite.prod.config.ts`  
✅ Updated all component imports to use `@services/api`  
✅ Updated api.ts to use `@/config`  
✅ Verified no relative paths remain (except local imports)  

---

## Summary

Path aliases are now fully configured and all imports have been updated. Your codebase now follows modern best practices with clean, maintainable import statements! 🎉

**Key takeaways:**
- `@services/api` instead of `../services/api`
- `@/config` instead of `../config`
- Easy to extend with new aliases as needed
- Better developer experience and code readability

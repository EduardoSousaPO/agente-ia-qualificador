import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  // TEMPORÁRIO: Middleware simplificado para debug - permitir tudo
  return NextResponse.next()
}

  /* CÓDIGO ORIGINAL COMENTADO PARA DEBUG
  try {
    const supabase = createMiddlewareClient(req, res)
    const {
      data: { session },
    } = await supabase.auth.getSession()

    // Check if this is a tenant-scoped route
    const tenantSlugMatch = req.nextUrl.pathname.match(/^\/app\/([^\/]+)/)
    
    if (tenantSlugMatch) {
      const tenantSlug = tenantSlugMatch[1]
      
      // If user is not authenticated, redirect to login
      if (!session) {
        const redirectUrl = req.nextUrl.clone()
        redirectUrl.pathname = '/login'
        redirectUrl.searchParams.set('redirectTo', req.nextUrl.pathname)
        return NextResponse.redirect(redirectUrl)
      }

      // Add tenant slug to headers for downstream components
      const requestHeaders = new Headers(req.headers)
      requestHeaders.set('x-tenant-slug', tenantSlug)
      
      return NextResponse.next({
        request: {
          headers: requestHeaders,
        },
      })
    }

    // Handle auth routes - PERMITIR ACESSO LIVRE
    if (req.nextUrl.pathname.startsWith('/login') || req.nextUrl.pathname.startsWith('/signup')) {
      // Se já estiver logado, redirecionar para dashboard
      if (session) {
        return NextResponse.redirect(new URL('/', req.url))
      }
      // Se não estiver logado, permitir acesso
      return res
    }

    // Protected routes (non-tenant specific)
    const protectedRoutes = ['/dashboard', '/leads', '/conversations', '/settings']
    const isProtectedRoute = protectedRoutes.some(route => 
      req.nextUrl.pathname.startsWith(route)
    )

    if (isProtectedRoute && !session) {
      const redirectUrl = req.nextUrl.clone()
      redirectUrl.pathname = '/login'
      redirectUrl.searchParams.set('redirectTo', req.nextUrl.pathname)
      return NextResponse.redirect(redirectUrl)
    }

    return res
  } catch (error) {
    // Em caso de erro, permitir acesso (failsafe)
    console.error('Middleware error:', error)
    return res
  }
  */

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}